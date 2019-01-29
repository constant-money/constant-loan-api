from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from common.test_utils import AuthenticationUtils
from loan.factories import LoanProgramFactory, LoanMemberFactory


class LoanApplicationTests(APITestCase):
    def setUp(self):
        self.auth_utils = AuthenticationUtils(self.client)
        self.auth_utils.user_login()
        self.url = reverse('loan:loan-application-view')

        LoanProgramFactory()
        LoanMemberFactory(user_email=self.auth_utils.username,
                          phone_retry=-999)

    def test_add_application(self):
        response = self.client.post(self.url, data={
            'loan_amount': 100,
            'term': 6,
            'members': [{
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
            }],
        }, format='json')

        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoanApplicationPhoneValidationTests(APITestCase):
    def setUp(self):
        self.auth_utils = AuthenticationUtils(self.client)
        self.auth_utils.user_login()
        self.url = reverse('loan:loan-application-view')

        LoanProgramFactory()

    def test_add_application_invalid_phone_verification(self):
        LoanMemberFactory(user_email=self.auth_utils.username,
                          phone_retry=10,
                          phone_verification_code='123456')

        response = self.client.post(self.url, data={
            'phone_verification_code': '111111'
        }, format='json')

        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_application(self):
        LoanMemberFactory(user_email=self.auth_utils.username,
                          phone_retry=10,
                          phone_verification_code='123456')

        response = self.client.post(self.url, data={
            'loan_amount': 100,
            'term': 6,
            'members': [{
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
            }],
            'phone_verification_code': '123456'
        }, format='json')

        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
