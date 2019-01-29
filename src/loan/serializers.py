from rest_framework import serializers

from loan.models import LoanApplication, LoanMemberApplication, LoanMember, LoanMemberApplicationDataField


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

    members = LoanMemberApplicationSerializer(source='loan_member_applications', many=True, read_only=True)
