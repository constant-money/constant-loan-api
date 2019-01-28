from rest_framework import authentication
from rest_framework.authentication import get_authorization_header

from integration_3rdparty.const import client
from loan.models import ConstUser


class LoanAuthentication(authentication.BaseAuthentication):
    keyword = 'bearer'

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        user_data = client.get_profile(auth[1].decode())['Result']
        user = ConstUser(
            user_id=user_data['ID'],
            username=user_data['UserName'],
            first_name=user_data['FullName'],
            email=user_data['Email'],
            dob=user_data['DOB'],
            constant_balance=user_data['ConstantBalance'],
            constant_balance_holding=user_data['ConstantBalanceHolding'],
            verified_level=user_data['VerifiedLevel'],
        )

        return user, None
