from model_utils import Choices

EMAIL_PURPOSE = Choices(
    ('email_verification', 'Email verification'),
)

SMS_PURPOSE = Choices(
    ('phone_verification', 'Phone verification'),
)

NOTIFICATION_METHOD = Choices(
    ('email', 'Email'),
    ('slack', 'Slack'),
    ('sms', 'SMS'),
    ('call', 'Call'),
)

LANGUAGE = Choices(
    ('en', 'English'),
    ('vi', 'Tiếng Việt'),
)
