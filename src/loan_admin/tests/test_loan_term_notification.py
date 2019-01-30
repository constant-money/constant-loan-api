from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from common.test_utils import AuthenticationUtils
from loan.factories import LoanTermNotificationFactory


class ListLoanTermTests(APITestCase):
    def setUp(self):
        self.auth_utils = AuthenticationUtils(self.client)
        self.auth_utils.admin_login()

        LoanTermNotificationFactory.create_batch(10)

    def test_list(self):
        url = reverse('loan-admin:loantermnotification-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 10)
        # print(response.json())
