from django.db.models import F

from common.business import generate_random_digit
from loan.constants import LOAN_APPLICATION_STATUS
from loan.exceptions import InvalidVerificationException, AlreadyVerifiedException, ExceedLimitException, \
    AlreadyInAnotherApplicationException
from loan.models import LoanMember, LoanMemberApplication

# Extend class to do business of model
from notification.constants import SMS_PURPOSE, LANGUAGE
from notification.provider.sms import SmsNotification


class LoanMemberBusiness(LoanMember):
    class Meta:
        proxy = True

    def is_phone_verified(self):
        return self.phone_retry == -999

    def verify_phone(self, code):
        if code != self.phone_verification_code:
            raise InvalidVerificationException
        self.phone_retry = -999
        self.save()

    def send_phone_verification_code(self, phone, language=LANGUAGE.en):
        if self.is_phone_verified():
            raise AlreadyVerifiedException
        if self.phone_retry == 0:
            raise ExceedLimitException

        self.phone_verification_code = generate_random_digit(6)

        SmsNotification.send_sms_template(phone,
                                          SMS_PURPOSE.phone_verification,
                                          language,
                                          {'code': self.phone_verification_code})

        self.user_phone = phone
        self.phone_retry = F('phone_retry') - 1
        self.save()

    def validate_active(self):
        # Check if there is active member in an active application
        if LoanMemberApplication.objects.filter(member=self, application__status__in=[
            LOAN_APPLICATION_STATUS.created,
            LOAN_APPLICATION_STATUS.pending,
            LOAN_APPLICATION_STATUS.processing,
            LOAN_APPLICATION_STATUS.approved,
        ]).count():
            raise AlreadyInAnotherApplicationException
