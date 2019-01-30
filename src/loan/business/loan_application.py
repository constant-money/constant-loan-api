from django.db import transaction
from django.db.models import Count, Q
from rest_framework.exceptions import ValidationError

from loan.constants import LOAN_APPLICATION_STATUS, LOAN_MEMBER_APPLICATION_STATUS
from loan.exceptions import InvalidStatusException
from loan.models import LoanApplication, LoanMember, LoanMemberApplication

# Extend class to do business of model
from notification.constants import EMAIL_PURPOSE, LANGUAGE
from notification.provider.email import EmailNotification


class LoanApplicationBusiness(LoanApplication):
    class Meta:
        proxy = True

    def approve(self):
        if self.status != LOAN_APPLICATION_STATUS.pending:
            raise InvalidStatusException

        self.status = LOAN_APPLICATION_STATUS.approved

        # TODO Generate term & Transfer CONST

        self.save()

    def reject(self, note=''):
        if self.status not in [LOAN_APPLICATION_STATUS.created, LOAN_APPLICATION_STATUS.pending]:
            raise InvalidStatusException

        self.status = LOAN_APPLICATION_STATUS.rejected
        self.note = note
        self.save()

    def cancel(self, note=''):
        if self.status not in [LOAN_APPLICATION_STATUS.created, LOAN_APPLICATION_STATUS.pending]:
            raise InvalidStatusException

        self.status = LOAN_APPLICATION_STATUS.cancelled
        self.note = note
        self.save()

    def send_connect_email(self, language=LANGUAGE.en):
        loan_members = LoanMember.objects\
            .filter(loan_member_members__main=False,
                    loan_member_members__application=self)\
            .exclude(loan_member_members__status=LOAN_MEMBER_APPLICATION_STATUS.connected)

        for loan_member in loan_members:
            EmailNotification.send_email_template(loan_member.user_email,
                                                  EMAIL_PURPOSE.email_connection,
                                                  language,
                                                  {'code': '{}_{}_{}'.format(
                                                      self.created_at.timestamp(),
                                                      self.id,
                                                      loan_member.id)}
                                                  )
            loan_member_application = LoanMemberApplication.objects.get(application=self,
                                                                        member=loan_member)
            loan_member_application.status = LOAN_MEMBER_APPLICATION_STATUS.connecting
            loan_member_application.save()

    @staticmethod
    @transaction.atomic
    def connect(code):
        parts = code.split('_')
        if len(parts) < 3:
            raise ValidationError

        created_at = parts[0]
        application_id = parts[1]
        loan_member_id = parts[2]

        application = LoanApplication.objects.get(id=application_id)
        if str(application.created_at.timestamp()) != created_at:
            raise ValidationError
        else:
            loan_member_application = LoanMemberApplication.objects.get(application=application,
                                                                        member=loan_member_id)
            loan_member_application.status = LOAN_MEMBER_APPLICATION_STATUS.connected
            loan_member_application.save()

            all_qs = LoanMemberApplication.objects.filter(application=application, main=False)
            connected_qs = all_qs.filter(status=LOAN_MEMBER_APPLICATION_STATUS.connected)

            # All connected
            if all_qs.count() == connected_qs.count():
                main = LoanMemberApplication.objects.get(application=application, main=True)
                main.status = LOAN_MEMBER_APPLICATION_STATUS.connected
                main.save()
                application.status = LOAN_APPLICATION_STATUS.pending
                application.save()
