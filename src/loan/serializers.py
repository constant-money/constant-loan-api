from rest_framework import serializers

from common.business import get_now
from loan.models import LoanApplication, LoanMemberApplication, LoanMember, LoanMemberApplicationDataField, LoanTerm, \
    LoanTermNotification, LoanProgram


class LoanProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanProgram
        fields = ('rate', 'min_term', 'max_term', 'cycle')


class LoanMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanMember
        exclude = ('phone_verification_code', 'phone_retry')


class LoanMemberApplicationDataFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanMemberApplicationDataField
        exclude = ('loan_applicant', )


class LoanMemberApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanMemberApplication
        fields = '__all__'
        read_only_fields = ('application',)

    member = LoanMemberSerializer()
    data_fields = LoanMemberApplicationDataFieldSerializer(source='applicant_data_fields',
                                                           many=True, read_only=True)


class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = '__all__'
        read_only_fields = ('rate', 'member_required', 'member_allowed', 'cycle', 'note')

    main_member = serializers.SerializerMethodField(read_only=True)

    def get_main_member(self, instance):
        member_app = LoanMemberApplication.objects.filter(application=instance,
                                                          main=True).first()

        return LoanMemberApplicationSerializer(member_app).data

    members = serializers.SerializerMethodField(read_only=True)

    def get_members(self, instance):
        member_apps = LoanMemberApplication.objects.filter(application=instance,
                                                           main=False)

        return [LoanMemberApplicationSerializer(member_app).data for member_app in member_apps]


class LoanTermNotificationSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanTermNotification
        exclude = ('loan_term', 'notification_note')


class LoanTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanTerm
        fields = '__all__'

    due_days = serializers.SerializerMethodField(source='get_due_days', read_only=True)
    loan_term_notifications = LoanTermNotificationSimpleSerializer(many=True, read_only=True)

    def get_due_days(self, instance):
        return (get_now() - instance.pay_date).days


class LoanTermNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanTermNotification
        fields = '__all__'


class LoanTermAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanTerm
        fields = '__all__'

    main_member = LoanMemberSerializer(source='loan_applicant.member', read_only=True)
    members = serializers.SerializerMethodField(read_only=True)
    due_days = serializers.SerializerMethodField(source='get_due_days', read_only=True)
    notification = serializers.SerializerMethodField(source='get_notification', read_only=True)

    def get_due_days(self, instance):
        return (get_now() - instance.pay_date).days

    def get_members(self, instance):
        members = LoanMember.objects.filter(loan_member_members__application=instance.loan_applicant.application,
                                            loan_member_members__main=False)

        return [LoanMemberSerializer(member).data for member in members]

    def get_notification(self, instance):
        obj = LoanTermNotification.objects.filter(loan_term=instance).order_by('id').last()
        if obj:
            return LoanTermNotificationSerializer(obj).data

        return None
