from model_utils import Choices

LOAN_APPLICATION_STATUS = Choices(
    ('created', 'Created'),
    ('pending', 'Pending'),
    ('processing', 'Processing'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('cancelled', 'Cancelled'),
    ('closed', 'Closed'),
)

LOAN_STATUS = Choices(
    ('active', 'Active'),
    ('completed', 'Completed'),
    ('overdue', 'Overdue'),
)

LOAN_TERM_STATUS = Choices(
    ('early_paid', 'Early Paid'),
    ('paid', 'Paid'),
    ('late', 'Late'),
    ('late_paid', 'Late Paid'),
)

FIELD_TYPE = Choices(
    ('number', 'Number'),
    ('text', 'Text'),
    ('image', 'Image'),
    ('file', 'File'),
)

LOAN_MEMBER_APPLICATION_STATUS = Choices(
    ('connecting', 'Connecting'),
    ('connected', 'Connected'),
    ('disconnected', 'Disconnected'),
)

LOAN_TERM_NOTIFICATION_STATUS = Choices(
    ('not_yet', 'Not Yet'),
    ('called', 'Called'),
    ('email_sent', 'Email Sent'),
)
