from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from common.test_utils import AuthenticationUtils
from loan.constants import LOAN_APPLICATION_STATUS
from loan.factories import LoanApplicationFactory


class ListPlanApplicationTests(APITestCase):
    def setUp(self):
        self.auth_utils = AuthenticationUtils(self.client)
        self.auth_utils.admin_login()

        LoanApplicationFactory.create_batch(10)

    def test_list(self):
        url = reverse('loan-admin:loanapplication-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 10)

    def test_filter_1(self):
        url = reverse('loan-admin:loanapplication-list')
        response = self.client.get(url, data={'status': LOAN_APPLICATION_STATUS.pending}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 3)


class PlanApplicationActionTests(APITestCase):
    def setUp(self):
        self.auth_utils = AuthenticationUtils(self.client)
        self.auth_utils.admin_login()

    def test_approve(self):
        loan_app = LoanApplicationFactory(status=LOAN_APPLICATION_STATUS.pending)
        url = reverse('loan-admin:loanapplication-approve', args=[loan_app.pk])
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], LOAN_APPLICATION_STATUS.approved)

    def test_reject(self):
        loan_app = LoanApplicationFactory(status=LOAN_APPLICATION_STATUS.pending)
        url = reverse('loan-admin:loanapplication-reject', args=[loan_app.pk])
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], LOAN_APPLICATION_STATUS.rejected)
