from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from common.http import StandardPagination
from loan.business.loan_application import LoanApplicationBusiness
from loan.models import LoanApplication
from loan.serializers import LoanApplicationSerializer
from loan_auth.authentication import AdminPermission


class LoanApplicationViewSet(mixins.RetrieveModelMixin,
                             mixins.ListModelMixin,
                             GenericViewSet):
    permission_classes = (IsAuthenticated, AdminPermission)

    serializer_class = LoanApplicationSerializer
    pagination_class = StandardPagination
    queryset = LoanApplication.objects.all().order_by('-created_at')
    filterset_fields = (
        'status',
    )

    @action(detail=True, methods=['patch'])
    def approve(self, request, pk=None):
        loan_application = LoanApplicationBusiness.objects.get(pk=pk)
        serializer = LoanApplicationSerializer(loan_application, data={}, partial=True)
        serializer.is_valid(True)
        loan_application.approve()

        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def reject(self, request, pk=None):
        loan_application = LoanApplicationBusiness.objects.get(pk=pk)
        serializer = LoanApplicationSerializer(loan_application, data={}, partial=True)
        serializer.is_valid(True)
        loan_application.reject(note=request.data.get('note', ''))

        return Response(serializer.data)
