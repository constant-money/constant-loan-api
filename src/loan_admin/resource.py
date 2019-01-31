from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from common.business import get_now
from common.http import StandardPagination
from loan.business.loan_application import LoanApplicationBusiness
from loan.models import LoanApplication, LoanTerm, LoanTermNotification
from loan.serializers import LoanApplicationSerializer, LoanTermAdminSerializer, LoanTermNotificationSerializer
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

    @action(detail=True, methods=['put'])
    def approve(self, request, pk=None):
        loan_application = LoanApplicationBusiness.objects.get(pk=pk)
        serializer = LoanApplicationSerializer(loan_application, data={}, partial=True)
        serializer.is_valid(True)
        loan_application.approve()

        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def reject(self, request, pk=None):
        loan_application = LoanApplicationBusiness.objects.get(pk=pk)
        serializer = LoanApplicationSerializer(loan_application, data={}, partial=True)
        serializer.is_valid(True)
        loan_application.reject(note=request.data.get('note', ''))

        return Response(serializer.data)


class LoanTermViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    permission_classes = (IsAuthenticated, AdminPermission)

    serializer_class = LoanTermAdminSerializer
    pagination_class = StandardPagination
    queryset = LoanTerm.objects.all()
    filterset_fields = (
        'paid_status',
    )

    def get_queryset(self):
        overdue = self.request.query_params.get('overdue')
        qs = LoanTerm.objects.select_related('loan_applicant__application').all().order_by('-created_at')
        if overdue is not None:
            qs = qs.filter(pay_date__lte=get_now())

        return qs


class LoanTermNotificationViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, AdminPermission)

    serializer_class = LoanTermNotificationSerializer
    pagination_class = StandardPagination
    queryset = LoanTermNotification.objects.all().order_by('-created_at')
    filterset_fields = (
        'loan_term',
    )
