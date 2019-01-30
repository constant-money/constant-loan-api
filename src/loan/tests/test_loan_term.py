from datetime import timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from common.business import get_now
from common.test_utils import AuthenticationUtils
from loan.factories import LoanApplicationFactory, LoanMemberFactory, LoanMemberApplicationFactory, \
    LoanTermFactory


class ListLoanTermTests(APITestCase):
    def setUp(self):
        self.auth_utils = AuthenticationUtils(self.client)
        self.auth_utils.user_login()

        LoanTermFactory.create_batch(10)

    def test_list(self):
        url = reverse('loan:loanterm-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 0)

    def test_user_list(self):
        url = reverse('loan:loanterm-list')
        member = LoanMemberFactory(user_id=1)
        app = LoanApplicationFactory()
        mem_app = LoanMemberApplicationFactory(application=app, member=member, main=True)
        LoanTermFactory(loan_applicant=mem_app, pay_date=get_now() + timedelta(days=2))

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)


class LoanTermTests(APITestCase):
    def setUp(self):
        self.auth_utils = AuthenticationUtils(self.client)
        self.auth_utils.user_login()

        member = LoanMemberFactory(user_id=1)
        app = LoanApplicationFactory()
        mem_app = LoanMemberApplicationFactory(application=app, member=member, main=True)
        self.loan_term = LoanTermFactory(loan_applicant=mem_app, pay_date=get_now() + timedelta(days=2))

    def test_pay(self):
        url = reverse('loan:loanterm-pay', args=[self.loan_term.pk])
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
