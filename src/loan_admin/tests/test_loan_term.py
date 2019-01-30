from datetime import timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from common.business import get_now
from common.test_utils import AuthenticationUtils
from loan.constants import LOAN_TERM_STATUS
from loan.factories import LoanApplicationFactory, LoanMemberFactory, LoanMemberApplicationFactory, \
    LoanTermFactory


class ListLoanTermTests(APITestCase):
    def setUp(self):
        self.auth_utils = AuthenticationUtils(self.client)
        self.auth_utils.admin_login()

        LoanTermFactory.create_batch(10)

    def test_list(self):
        url = reverse('loan-admin:loanterm-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 10)

    def test_filter_1(self):
        url = reverse('loan-admin:loanterm-list')
        response = self.client.get(url, data={'paid_status': LOAN_TERM_STATUS.early_paid}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(len(response.json()['results']), 10)

    def test_full_detail(self):
        url = reverse('loan-admin:loanterm-list')
        member = LoanMemberFactory()
        member_sub1 = LoanMemberFactory()
        member_sub2 = LoanMemberFactory()
        app = LoanApplicationFactory()
        mem_app = LoanMemberApplicationFactory(application=app, member=member, main=True)
        LoanMemberApplicationFactory(application=app, member=member_sub1, main=False)
        LoanMemberApplicationFactory(application=app, member=member_sub2, main=False)
        LoanTermFactory(loan_applicant=mem_app, pay_date=get_now() + timedelta(days=2))

        response = self.client.get(url, format='json')
        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
