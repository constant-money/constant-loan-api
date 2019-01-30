from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from common.http import StandardPagination
from loan.business.loan_application import LoanApplicationBusiness
from loan.business.loan_term import LoanTermBusiness
from loan.models import LoanTerm, LoanApplication
from loan.serializers import LoanApplicationSerializer, LoanTermSerializer


class LoanApplicationViewSet(mixins.RetrieveModelMixin,
                             mixins.ListModelMixin,
                             GenericViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = LoanApplicationSerializer
    pagination_class = StandardPagination
    queryset = LoanApplication.objects.none()
    filterset_fields = (
        'status',
    )

    def get_queryset(self):
        qs = LoanApplication.objects.filter(members__user_id=self.request.user.user_id).order_by('-created_at')

        return qs

    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        loan_application = LoanApplicationBusiness.objects.get(pk=pk, members__user_id=self.request.user.user_id)
        serializer = LoanApplicationSerializer(loan_application, data={}, partial=True)
        serializer.is_valid(True)
        loan_application.cancel(note=request.data.get('note', ''))

        return Response(serializer.data)


class LoanTermViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    permission_classes = (IsAuthenticated, )

    serializer_class = LoanTermSerializer
    pagination_class = StandardPagination
    queryset = LoanTerm.objects.none()
    filterset_fields = (
        'paid_status',
        'loan_applicant__application'
    )

    def get_queryset(self):
        qs = LoanTerm.objects.select_related('loan_applicant__application')\
            .filter(loan_applicant__member__user_id=self.request.user.user_id).order_by('-created_at')

        return qs

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        loan_term = LoanTermBusiness.objects.get(pk=pk, loan_applicant__member__user_id=request.user.user_id)
        serializer = LoanTermSerializer(loan_term, data={}, partial=True)
        serializer.is_valid(True)
        loan_term.pay()

        return Response(serializer.data)
