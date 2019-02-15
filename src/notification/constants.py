from model_utils import Choices

EMAIL_PURPOSE = Choices(
    ('email_connection', 'Email connection'),
    ('term_reminder', 'Term reminder'),
    ('not_enough_balance', 'Not enough balance'),
)

SMS_PURPOSE = Choices(
    ('phone_verification', 'Phone verification'),
    ('term_reminder', 'Term reminder'),
    ('not_enough_balance', 'Not enough balance'),
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
