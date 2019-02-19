import logging
from datetime import timedelta

from django.db import transaction
from django.db.models import Count, Q
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.business import get_now
from constant_core.exceptions import NotEnoughBalanceException
from loan.business.loan_application import LoanApplicationBusiness
from loan.business.loan_member import LoanMemberBusiness
from loan.business.loan_member_application import LoanMemberApplicationBusiness
from loan.business.loan_term import LoanTermBusiness
from loan.constants import LOAN_MEMBER_APPLICATION_STATUS, LOAN_APPLICATION_STATUS
from loan.exceptions import InvalidEmailException, DuplicatedEmailInFormException
from loan.models import LoanProgram
from loan.serializers import LoanApplicationSerializer, LoanMemberApplicationSerializer, \
    LoanMemberApplicationDataFieldSerializer, LoanMemberSerializer
from notification.constants import LANGUAGE


class StartView(APIView):
    def get(self, request, format=None):
        return Response('API works')


class SampleAuthView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        return Response()


class PhoneVerificationView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        member = LoanMemberBusiness.objects.filter(user_email=request.user.email).first()
        if not member:
            return Response({
                'phone_verified': False
            })

        return Response({
            'user_phone': member.user_phone,
            'phone_verified': member.is_phone_verified()
        })

    def post(self, request, format=None):
        member = LoanMemberBusiness.objects.filter(user_email=request.user.email).first()
        if not member:
            # New user, create one
            user = request.user
            member = LoanMemberBusiness.objects.create(
                user_id=user.id,
                user_email=user.email,
                user_name=user.first_name,
            )

        user_phone = request.data.get('user_phone')
        if not user_phone:
            raise ValidationError

        member.send_phone_verification_code(user_phone, request.data.get('language', LANGUAGE.en))

        return Response(
            True
        )


class LoanApplicationCheckView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        member = LoanMemberBusiness.objects.filter(user_email=request.user.user_id).first()
        can_submit_form = True
        if member:
            can_submit_form = not member.check_active()

        return Response({
            'can_submit_form': can_submit_form
        })


class LoanApplicationView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        member = LoanMemberBusiness.objects.filter(user_email=request.user.email).first()
        if not member.is_phone_verified():
            member.verify_phone(request.data.get('phone_verification_code'))

        loan_app_serializer = LoanApplicationSerializer(data=request.data)
        loan_app_serializer.is_valid(True)

        if not request.data.get('main_member'):
            raise ValidationError
        if not request.data.get('members'):
            raise ValidationError

        loan_member_app_serializers = self._extract_data_to_serializers(request)
        self._persistent_serializer(request, loan_app_serializer, loan_member_app_serializers)

        return Response(loan_app_serializer.data, status.HTTP_201_CREATED)

    @staticmethod
    @transaction.atomic
    def _extract_data_to_serializers(request):
        loan_app_members = request.data['members']
        loan_app_members.insert(0, request.data['main_member'])
        loan_member_app_serializers = []
        emails = []
        for loan_app_member in loan_app_members:
            data = {
                'loan_member': None,
                'loan_member_app': None,
                'data_fields': []
            }

            loan_member_data = loan_app_member.get('member')
            if not loan_member_data:
                raise ValidationError
            email = loan_member_data.get('user_email')
            if email:
                email_tail = email.split('@')[-1]
                if '.edu' not in email_tail and 'grr.la' not in email_tail:
                    raise InvalidEmailException
                if email in emails:
                    raise DuplicatedEmailInFormException
                emails.append(email)
            else:
                raise InvalidEmailException

            loan_member = LoanMemberBusiness.objects.filter(user_email=loan_member_data.get('user_email')).first()
            if loan_member:
                loan_member.validate_active()
                loan_member_serializer = LoanMemberSerializer(loan_member, data=loan_member_data, partial=True)
            else:
                loan_member_serializer = LoanMemberSerializer(data=loan_member_data)
            loan_member_serializer.is_valid(True)
            data['loan_member'] = loan_member_serializer

            loan_member_app_serializer = LoanMemberApplicationSerializer(data=loan_app_member)
            loan_member_app_serializer.is_valid(True)
            data['loan_member_app'] = loan_member_app_serializer

            data_fields = loan_app_member.get('data_fields', [])
            for data_field in data_fields:
                data_field_serializer = LoanMemberApplicationDataFieldSerializer(data=data_field)
                data_field_serializer.is_valid(True)
                data['data_fields'].append(data_field_serializer)

            loan_member_app_serializers.append(data)
        return loan_member_app_serializers

    @staticmethod
    def _persistent_serializer(request, loan_app_serializer, loan_member_app_serializers):
        # Persistent
        program = LoanProgram.objects.first()
        loan_term = loan_app_serializer.validated_data['term']
        if program.min_term < loan_term < program.max_term:
            raise ValidationError

        loan_app = loan_app_serializer.save(
            program=program,
            member_required=program.max_member,
            member_allowed=1,
            rate=program.rate,
            cycle=program.cycle,
        )
        # First item is the main one
        main = True
        for loan_member_app_item in loan_member_app_serializers:
            loan_member_serializer = loan_member_app_item['loan_member']
            user_id = None
            if main:
                user_id = request.user.user_id
            loan_member = loan_member_serializer.save(user_id=user_id)

            loan_member_app_serializer = loan_member_app_item['loan_member_app']
            loan_member_app = loan_member_app_serializer.save(
                application=loan_app,
                member=loan_member,
                main=main,
                status=LOAN_MEMBER_APPLICATION_STATUS.connecting if main else None,
            )
            main = False

            for data_field_serializer in loan_member_app_item['data_fields']:
                data_field_serializer.save(loan_applicant=loan_member_app)

        loan_application = LoanApplicationBusiness.objects.get(id=loan_app.id)
        loan_application.send_connect_email(request.query_params.get('language', LANGUAGE.en))


class LoanConnectView(APIView):
    def get(self, request, format=None):
        code = request.query_params.get('code')
        if not code:
            raise ValidationError

        LoanApplicationBusiness.connect(code)

        return Response(True)


class LoanDisconnectView(APIView):
    def get(self, request, format=None):
        code = request.query_params.get('code')
        if not code:
            raise ValidationError

        LoanApplicationBusiness.connection_reject(code)

        return Response(True)


class LoanTermReminderView(APIView):
    def post(self, request, format=None):
        now = get_now() + timedelta(days=10)
        # Get all
        terms = LoanTermBusiness.objects.filter(pay_date__day=now.day,
                                                pay_date__month=now.month,
                                                pay_date__year=now.year)
        for term in terms:
            try:
                term.send_email_reminder()
                term.send_sms_reminder()
            except Exception as ex:
                logging.exception(ex)


class LoanTermAutoPayView(APIView):
    def post(self, request, format=None):
        now = get_now()
        # Get all not pay yet
        terms = LoanTermBusiness.objects.filter(pay_date__day=now.day,
                                                pay_date__month=now.month,
                                                pay_date__year=now.year,
                                                paid=False)
        for term in terms:
            try:
                term.pay()
            except NotEnoughBalanceException:
                try:
                    term.send_email_not_enough_balance()
                    term.send_sms_not_enough_balance()
                except Exception as ex:
                    logging.exception(ex)
            except Exception as ex:
                logging.exception(ex)


class LoanApplicationConnectionReminderView(APIView):
    def post(self, request, format=None):
        now = get_now() - timedelta(days=3)
        connecting_members = LoanMemberApplicationBusiness.objects.filter(
            status=LOAN_MEMBER_APPLICATION_STATUS.connecting,
            application__created_at__day=now.day,
            application__created_at__month=now.month,
            application__created_at__year=now.year,
        )
        for member in connecting_members:
            try:
                member.send_email_connection_reminder()
                member.send_sms_connection_reminder()
            except Exception as ex:
                logging.exception(ex)


class LoanApplicationExpiredView(APIView):
    def post(self, request, format=None):
        now = get_now() - timedelta(days=7)
        connected_member_condition = Q(loan_member_applications__main=False) & \
            Q(loan_member_applications__status=LOAN_MEMBER_APPLICATION_STATUS.connected)
        ref_member_condition = Q(loan_member_applications__main=False)
        connected_member_count = Count('loan_member_applications',
                                       filter=connected_member_condition)
        ref_member_count = Count('loan_member_applications',
                                 filter=ref_member_condition)

        applications = LoanApplicationBusiness.objects\
            .filter(status=LOAN_APPLICATION_STATUS.created,
                    created_at__day=now.day,
                    created_at__month=now.month,
                    created_at__year=now.year)\
            .annotate(connected_member_count=connected_member_count,
                      ref_member_count=ref_member_count)

        for application in applications:
            if application.connected_member_count < application.ref_member_count:
                application.reject()
