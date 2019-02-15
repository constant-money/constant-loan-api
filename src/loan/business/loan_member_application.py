from loan.models import LoanMemberApplication
from notification.constants import LANGUAGE, EMAIL_PURPOSE, SMS_PURPOSE
from notification.provider.email import EmailNotification
from notification.provider.sms import SmsNotification


class LoanMemberApplicationBusiness(LoanMemberApplication):
    class Meta:
        proxy = True

    def send_email_connection_reminder(self, language: str = LANGUAGE.en):
        EmailNotification.send_email_template(self.member.user_email,
                                              EMAIL_PURPOSE.connection_reminder,
                                              language,
                                              {}
                                              )

    def send_sms_connection_reminder(self, language: str = LANGUAGE.en):
        SmsNotification.send_sms_template(self.member.user_phone,
                                          SMS_PURPOSE.connection_reminder,
                                          language,
                                          {})
