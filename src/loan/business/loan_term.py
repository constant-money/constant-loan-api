from django.conf import settings
from django.db import transaction

from common.business import get_now
from constant_core.business import ConstantCoreBusiness
from loan.business.loan_application import LoanApplicationBusiness
from loan.constants import LOAN_TERM_STATUS
from loan.exceptions import AlreadyPaidException
from loan.models import LoanTerm, LoanPayment


# Extend class to do business of model
from notification.constants import EMAIL_PURPOSE, LANGUAGE, SMS_PURPOSE
from notification.provider.email import EmailNotification
from notification.provider.sms import SmsNotification


class LoanTermBusiness(LoanTerm):
    class Meta:
        proxy = True

    @transaction.atomic
    def pay(self):
        if self.paid:
            raise AlreadyPaidException

        ConstantCoreBusiness.transfer(self.loan_applicant.member.user_id,
                                      settings.CONSTANT_USER_ID, self.total_amount)

        now = get_now()
        self.paid_date = now
        self.paid = True
        if self.paid_date < self.pay_date:
            self.paid_status = LOAN_TERM_STATUS.paid
        else:
            self.paid_status = LOAN_TERM_STATUS.late_paid

        obj = LoanPayment.objects.create(
            loan_applicant=self.loan_applicant,
            paid_amount=self.total_amount,
            original_amount=self.original_amount,
            interest_amount=self.interest_amount,
            fee=0
        )

        self.payment = obj
        self.save()

        # All paid, close application
        all_term = LoanTerm.objects.filter(loan_applicant=self.loan_applicant).count()
        paid_term = LoanTerm.objects.filter(loan_applicant=self.loan_applicant, paid=True).count()
        if all_term == paid_term:
            LoanApplicationBusiness.objects.get(id=self.loan_applicant.application.id).close()

            # TODO Give credit point here

    def send_email_reminder(self, language: str = LANGUAGE.en):
        EmailNotification.send_email_template(self.loan_applicant.member.user_email,
                                              EMAIL_PURPOSE.term_reminder,
                                              language,
                                              {}
                                              )

    def send_sms_reminder(self, language: str = LANGUAGE.en):
        SmsNotification.send_sms_template(self.loan_applicant.member.user_phone,
                                          SMS_PURPOSE.term_reminder,
                                          language,
                                          {})
