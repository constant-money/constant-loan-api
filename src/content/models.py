from django.db import models
from tinymce.models import HTMLField

from loan.models import TimestampedModel
from notification.constants import EMAIL_PURPOSE, SMS_PURPOSE, LANGUAGE


class EmailContent(TimestampedModel):
    class Meta:
        unique_together = ('purpose', 'language')
        verbose_name = 'Email Content'
        verbose_name_plural = 'Email Contents'

    purpose = models.CharField(max_length=100, choices=EMAIL_PURPOSE)
    language = models.CharField(max_length=20, choices=LANGUAGE, blank=True)
    subject = models.CharField(max_length=500)
    content = HTMLField()


class SMSContent(TimestampedModel):
    class Meta:
        unique_together = ('purpose', 'language')
        verbose_name = 'SMS Content'
        verbose_name_plural = 'SMS Contents'

    purpose = models.CharField(max_length=100, choices=SMS_PURPOSE)
    language = models.CharField(max_length=20, choices=LANGUAGE, blank=True)
    content = models.CharField(max_length=200)
