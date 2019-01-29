from unittest.mock import MagicMock

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from common.test_utils import AuthenticationUtils
from loan.factories import LoanMemberFactory
from loan.models import LoanMember
from notification.provider.sms import SmsNotification


class LoanMemberPhoneVerificationTests(APITestCase):
    def setUp(self):
        self.auth_utils = AuthenticationUtils(self.client)
        self.auth_utils.user_login()

    def test_check_phone_verfication_no_member(self):
        url = reverse('loan:phone-verification-view')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['phone_verified'], False)

    def test_check_phone_verification_has_member(self):
        LoanMemberFactory(user_email=self.auth_utils.username)

        url = reverse('loan:phone-verification-view')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['phone_verified'], False)

    def test_check_phone_verification_has_member_verified(self):
        LoanMemberFactory(user_email=self.auth_utils.username, phone_retry=-999)

        url = reverse('loan:phone-verification-view')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['phone_verified'], True)


class LoanMemberSendPhoneVerificationTests(APITestCase):
    def setUp(self):
        SmsNotification.send_sms_template = MagicMock(return_value=None)
        self.auth_utils = AuthenticationUtils(self.client)
        self.auth_utils.user_login()

    def test_send_no_member(self):
        self.assertEqual(LoanMember.objects.count(), 0)
        url = reverse('loan:phone-verification-view')

        user_phone = '1234567890'
        response = self.client.post(url, data={
            'user_phone': user_phone
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        member = LoanMember.objects.first()
        self.assertEqual(LoanMember.objects.count(), 1)
        self.assertEqual(member.user_phone, user_phone)

    def test_send_has_member(self):
        LoanMemberFactory(user_email=self.auth_utils.username, phone_retry=10)
        self.assertEqual(LoanMember.objects.count(), 1)
        url = reverse('loan:phone-verification-view')

        user_phone = '1234567890'
        response = self.client.post(url, data={
            'user_phone': user_phone
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        member = LoanMember.objects.first()
        self.assertEqual(LoanMember.objects.count(), 1)
        self.assertEqual(member.user_phone, user_phone)

    def test_send_has_member_limit(self):
        LoanMemberFactory(user_email=self.auth_utils.username, phone_retry=0)

        url = reverse('loan:phone-verification-view')

        user_phone = '1234567890'
        response = self.client.post(url, data={
            'user_phone': user_phone
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
