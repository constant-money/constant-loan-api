from django.conf import settings

from content.models import SMSContent

from integration_3rdparty.twilio import send_sms


class SmsNotification(object):
    @staticmethod
    def send_sms_template(to_phone: str, content_key: str, language: str, params: dict = None,
                          raise_exception: bool = False):
        obj = SMSContent.objects.get(purpose=content_key, language=language)
        content = obj.content
        if params:
            content = content.format(**params)

        SmsNotification.send_sms(to_phone, content, raise_exception)

    @staticmethod
    def send_sms(to_phone: str, content: str, raise_exception: bool = False):
        try:
            send_sms(settings.FROM_PHONE_NUMBER, to_phone, content)
        except Exception:
            if raise_exception:
                raise
