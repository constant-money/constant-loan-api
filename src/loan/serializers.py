from rest_framework import serializers

from loan.models import LoanApplication


class LoanApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanApplication
        fields = '__all__'
