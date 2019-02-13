from unittest.mock import MagicMock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from common.test_utils import AuthenticationUtils
from loan.constants import LOAN_APPLICATION_STATUS, LOAN_MEMBER_APPLICATION_STATUS
from loan.factories import LoanProgramFactory, LoanMemberFactory, LoanApplicationFactory, LoanMemberApplicationFactory
from loan.models import LoanMemberApplication, LoanApplication
from notification.provider.email import EmailNotification


class LoanApplicationTests(APITestCase):
    def setUp(self):
        self.auth_utils = AuthenticationUtils(self.client)
        self.auth_utils.user_login()
        self.url = reverse('loan:loan-application-view')

        EmailNotification.send_email_template = MagicMock(return_value=None)

        LoanProgramFactory()
        LoanMemberFactory(user_email=self.auth_utils.username,
                          phone_retry=-999)

    def test_add_application(self):
        response = self.client.post(self.url, data={
            'loan_amount': 100,
            'term': 6,
            'main_member': {
                'member': {
                    'user_email': 'student@mail.edu',
                    'user_phone': '123456789',
                    'user_name': 'Student Name',
                },
                'data_fields': [{
                    'field_name': 'student_id',
                    'field_value': '123456789000',
                    'field_type': 'text'
                }, {
                    'field_name': 'student_card',
                    'field_value': 'image_url',
                    'field_type': 'image'
                }]
            },
            'members': [{
                'member': {
                    'user_email': 'student1@mail.edu',
                    'user_phone': '123456789',
                    'user_name': 'Student Name',
                },
                'data_fields': [{
                    'field_name': 'student_id',
                    'field_value': '123456789000',
                    'field_type': 'text'
                }, {
                    'field_name': 'student_card',
                    'field_value': 'image_url',
                    'field_type': 'image'
                }]
            }],
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoanApplicationPhoneValidationTests(APITestCase):
    def setUp(self):
        self.auth_utils = AuthenticationUtils(self.client)
        self.auth_utils.user_login()
        self.url = reverse('loan:loan-application-view')

        EmailNotification.send_email_template = MagicMock(return_value=None)

        LoanProgramFactory()

    def test_add_application_invalid_phone_verification(self):
        LoanMemberFactory(user_email=self.auth_utils.username,
                          phone_retry=10,
                          phone_verification_code='123456')

        response = self.client.post(self.url, data={
            'phone_verification_code': '111111'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_application(self):
        LoanMemberFactory(user_email=self.auth_utils.username,
                          phone_retry=10,
                          phone_verification_code='123456')

        response = self.client.post(self.url, data={
            'loan_amount': 100,
            'term': 6,
            'main_member': {
                'member': {
                    'user_email': 'student@mail.edu',
                    'user_phone': '123456789',
                    'user_name': 'Student Name',
                },
                'data_fields': [{
                    'field_name': 'student_id',
                    'field_value': '123456789000',
                    'field_type': 'text'
                }, {
                    'field_name': 'student_card',
                    'field_value': 'image_url',
                    'field_type': 'image'
                }]
            },
            'members': [{
                'member': {
                    'user_email': 'student1@mail.edu',
                    'user_phone': '123456789',
                    'user_name': 'Student Name',
                },
                'data_fields': [{
                    'field_name': 'student_id',
                    'field_value': '123456789000',
                    'field_type': 'text'
                }, {
                    'field_name': 'student_card',
                    'field_value': 'image_url',
                    'field_type': 'image'
                }]
            }],
            'phone_verification_code': '123456'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ListLoanApplicationTests(APITestCase):
    def setUp(self):
        self.auth_utils = AuthenticationUtils(self.client)
        self.auth_utils.user_login()

        LoanApplicationFactory.create_batch(10)

    def test_list(self):
        url = reverse('loan:loanapplication-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 0)

    def test_user_list(self):
        url = reverse('loan:loanapplication-list')
        member = LoanMemberFactory(user_id=1)
        app = LoanApplicationFactory()
        LoanMemberApplicationFactory(application=app, member=member, main=True)

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)


class LoanApplicationActionTests(APITestCase):
    def setUp(self):
        self.auth_utils = AuthenticationUtils(self.client)
        self.auth_utils.user_login()

    def test_cancel(self):
        member = LoanMemberFactory(user_id=1)
        app = LoanApplicationFactory(status=LOAN_APPLICATION_STATUS.pending)
        loan_app = LoanMemberApplicationFactory(application=app, member=member, main=True)

        url = reverse('loan:loanapplication-cancel', args=[loan_app.pk])
        response = self.client.patch(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['status'], LOAN_APPLICATION_STATUS.cancelled)


class LoanApplicationConnectTests(APITestCase):
    def setUp(self):
        self.member1 = LoanMemberFactory(user_id=1)
        self.member2 = LoanMemberFactory(user_id=2)
        self.member3 = LoanMemberFactory(user_id=3)

        self.app = LoanApplicationFactory(status=LOAN_APPLICATION_STATUS.created)
        LoanMemberApplicationFactory(application=self.app, member=self.member1, main=True,
                                     status=LOAN_MEMBER_APPLICATION_STATUS.connecting)
        LoanMemberApplicationFactory(application=self.app, member=self.member2, main=False,
                                     status=LOAN_MEMBER_APPLICATION_STATUS.connecting)
        LoanMemberApplicationFactory(application=self.app, member=self.member3, main=False,
                                     status=LOAN_MEMBER_APPLICATION_STATUS.connecting)

        self.url = reverse('loan:loan-connect-view')

    def test_connect(self):
        response = self.client.get(self.url, data={
            'code': '{}_{}_{}'.format(
                self.app.created_at.timestamp(),
                self.app.id,
                self.member2.id,
            )}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_app = LoanApplication.objects.get(id=self.app.id)
        self.assertEqual(test_app.status, LOAN_APPLICATION_STATUS.created)
        test_member1 = LoanMemberApplication.objects.get(application=self.app.id, member=self.member1.id)
        self.assertEqual(test_member1.status, LOAN_MEMBER_APPLICATION_STATUS.connecting)
        test_member2 = LoanMemberApplication.objects.get(application=self.app.id, member=self.member2.id)
        self.assertEqual(test_member2.status, LOAN_MEMBER_APPLICATION_STATUS.connected)
        test_member3 = LoanMemberApplication.objects.get(application=self.app.id, member=self.member3.id)
        self.assertEqual(test_member3.status, LOAN_MEMBER_APPLICATION_STATUS.connecting)

    def test_connect_all(self):
        response = self.client.get(self.url, data={
            'code': '{}_{}_{}'.format(
                self.app.created_at.timestamp(),
                self.app.id,
                self.member2.id,
            )}, format='json')
        response = self.client.get(self.url, data={
            'code': '{}_{}_{}'.format(
                self.app.created_at.timestamp(),
                self.app.id,
                self.member3.id,
            )}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        test_app = LoanApplication.objects.get(id=self.app.id)
        self.assertEqual(test_app.status, LOAN_APPLICATION_STATUS.pending)
        test_member1 = LoanMemberApplication.objects.get(application=self.app.id, member=self.member1.id)
        self.assertEqual(test_member1.status, LOAN_MEMBER_APPLICATION_STATUS.connected)
        test_member2 = LoanMemberApplication.objects.get(application=self.app.id, member=self.member2.id)
        self.assertEqual(test_member2.status, LOAN_MEMBER_APPLICATION_STATUS.connected)
        test_member3 = LoanMemberApplication.objects.get(application=self.app.id, member=self.member3.id)
        self.assertEqual(test_member3.status, LOAN_MEMBER_APPLICATION_STATUS.connected)
