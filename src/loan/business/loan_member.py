from django.db.models import F

from common.business import generate_random_digit
from loan.exceptions import InvalidVerificationException, AlreadyVerifiedException, ExceedLimitException
from loan.models import LoanMember


# Extend class to do business of model
from notification.constants import SMS_PURPOSE, LANGUAGE
from notification.provider.sms import SmsNotification


class LoanMemberBusiness(LoanMember):
    class Meta:
        proxy = True

    def is_phone_verified(self):
        return self.phone_retry == -999

    def verify_phone(self, code):
        if code == self.phone_verification_code:
            self.phone_retry = -999
            self.save()

        raise InvalidVerificationException

    def send_phone_verification_code(self, language=LANGUAGE.en):
        if self.is_phone_verified():
            raise AlreadyVerifiedException
        if self.phone_retry == 0:
            raise ExceedLimitException

        SmsNotification.send_sms_template(self.user_phone,
                                          SMS_PURPOSE.phone_verification,
                                          language,
                                          {'code': self.phone_verification_code})

        self.phone_verification_code = generate_random_digit(6)
        self.phone_retry = F('phone_retry') - 1
        self.save()
