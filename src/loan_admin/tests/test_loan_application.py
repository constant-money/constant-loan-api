from unittest.mock import MagicMock

from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from common.test_utils import AuthenticationUtils
from constant_core.business import ConstantCoreBusiness
from loan.constants import LOAN_APPLICATION_STATUS, FIELD_TYPE
from loan.factories import LoanApplicationFactory, LoanMemberFactory, LoanMemberApplicationFactory, \
    LoanMemberApplicationDataFieldFactory


class ListLoanApplicationTests(APITestCase):
    def setUp(self):
        self.auth_utils = AuthenticationUtils(self.client)
        self.auth_utils.admin_login()

        LoanApplicationFactory.create_batch(20)

    def test_list(self):
        url = reverse('loan-admin:loanapplication-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 20)

    def test_filter_1(self):
        url = reverse('loan-admin:loanapplication-list')
        response = self.client.get(url, data={'status': LOAN_APPLICATION_STATUS.pending}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(len(response.json()['results']), 20)

    def test_full_detail(self):
        url = reverse('loan-admin:loanapplication-list')
        member = LoanMemberFactory()
        member_sub1 = LoanMemberFactory()
        member_sub2 = LoanMemberFactory()
        app = LoanApplicationFactory()
        mem_app = LoanMemberApplicationFactory(application=app, member=member, main=True)
        LoanMemberApplicationFactory(application=app, member=member_sub1, main=False)
        LoanMemberApplicationFactory(application=app, member=member_sub2, main=False)
        LoanMemberApplicationDataFieldFactory(loan_applicant=mem_app, field_type=FIELD_TYPE.text)
        LoanMemberApplicationDataFieldFactory(loan_applicant=mem_app, field_type=FIELD_TYPE.image)
        LoanMemberApplicationDataFieldFactory(loan_applicant=mem_app, field_type=FIELD_TYPE.file)

        response = self.client.get(url, format='json')
        # print(response.json())

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LoanApplicationActionTests(APITestCase):
    def setUp(self):
        self.auth_utils = AuthenticationUtils(self.client)
        self.auth_utils.admin_login()

    def test_approve(self):
        loan_app = LoanApplicationFactory(status=LOAN_APPLICATION_STATUS.pending)
        member = LoanMemberFactory()
        LoanMemberApplicationFactory(application=loan_app, member=member, main=True)
        ConstantCoreBusiness.transfer = MagicMock(return_value=None)

        url = reverse('loan-admin:loanapplication-approve', args=[loan_app.pk])
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], LOAN_APPLICATION_STATUS.approved)

        ConstantCoreBusiness.transfer.assert_called_once_with(settings.CONSTANT_USER_ID,
                                                              member.user_id, loan_app.loan_amount)

    def test_reject(self):
        loan_app = LoanApplicationFactory(status=LOAN_APPLICATION_STATUS.pending)

        url = reverse('loan-admin:loanapplication-reject', args=[loan_app.pk])
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], LOAN_APPLICATION_STATUS.rejected)
