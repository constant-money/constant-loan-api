from django.contrib.auth.models import User
from django.db import models

from loan.constants import (
    LOAN_APPLICATION_STATUS,
    LOAN_TERM_STATUS,
    LOAN_STATUS,
    FIELD_TYPE,
    LOAN_MEMBER_APPLICATION_STATUS,
    LOAN_TERM_NOTIFICATION_STATUS)


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ConstUser(User):
    class Meta:
        managed = False

    user_id = models.IntegerField()
    role_id = models.IntegerField()
    dob = models.CharField(max_length=50)
    verified_level = models.IntegerField(default=0)
    constant_balance = models.DecimalField(max_digits=12, decimal_places=2)
    constant_balance_holding = models.DecimalField(max_digits=12, decimal_places=2)


class LoanProgram(models.Model):
    class Meta:
        verbose_name = 'Loan Program'
        verbose_name_plural = 'Loan Programs'

    name = models.CharField(max_length=500)
    min_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    min_member = models.IntegerField()
    max_member = models.IntegerField()
    active = models.BooleanField(default=True)
    rate = models.DecimalField(max_digits=8, decimal_places=2)
    cycle = models.IntegerField()
    min_term = models.IntegerField(default=6)
    max_term = models.IntegerField(default=12)

    def __str__(self):
        return '{}'.format(self.name)


class LoanMember(TimestampedModel):
    class Meta:
        verbose_name = 'Loan Member'
        verbose_name_plural = 'Loan Members'

    user_name = models.CharField(max_length=255)
    user_email = models.CharField(max_length=255)
    user_id = models.IntegerField(null=True, blank=True)
    user_phone = models.CharField(max_length=20, null=True, blank=True)
    user_external_email = models.CharField(max_length=255, null=True, blank=True)
    credit = models.IntegerField(default=0)
    phone_verification_code = models.CharField(max_length=10, blank=True)
    phone_retry = models.IntegerField(default=10)

    def __str__(self):
        return '{}'.format(self.user_email)


class LoanApplication(TimestampedModel):
    class Meta:
        verbose_name = 'Loan Application'
        verbose_name_plural = 'Loan Applications'

    program = models.ForeignKey(LoanProgram, related_name='loan_applications', on_delete=models.SET_NULL,
                                null=True, blank=True)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    member_required = models.IntegerField(help_text='How many members required to apply to this loan')
    member_allowed = models.IntegerField(help_text='How many members allowed to loan per cycle')
    rate = models.DecimalField(max_digits=8, decimal_places=2, help_text='Loan rate')
    cycle = models.IntegerField(help_text='How many days need to pay the loan. For example 7 days')
    term = models.IntegerField(help_text='How many cycle need to pay the loan. For example 12 cycles')
    status = models.CharField(max_length=50, choices=LOAN_APPLICATION_STATUS, default=LOAN_APPLICATION_STATUS.created)
    members = models.ManyToManyField(LoanMember, through='LoanMemberApplication', related_name='applications_of_member')
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.program) if not self.members else self.members[0].user_email


class LoanMemberApplication(models.Model):
    class Meta:
        verbose_name = 'Loan Member In Application'
        verbose_name_plural = 'Loan Members In Applications'
        unique_together = ('application', 'member')

    application = models.ForeignKey(LoanApplication, related_name='loan_member_applications', on_delete=models.PROTECT)
    member = models.ForeignKey(LoanMember, related_name='loan_member_members', on_delete=models.PROTECT)
    main = models.BooleanField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=LOAN_MEMBER_APPLICATION_STATUS, null=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.member.user_email)


class LoanMemberApplicationDataField(models.Model):
    loan_applicant = models.ForeignKey(LoanMemberApplication,
                                       related_name='applicant_data_fields', on_delete=models.PROTECT)
    field_name = models.CharField(max_length=100)
    field_value = models.CharField(max_length=500)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPE, default=FIELD_TYPE.text)


class MemberCreditHistory(TimestampedModel):
    class Meta:
        verbose_name = 'Member Credit History'
        verbose_name_plural = 'Member Credit Histories'

    member = models.ForeignKey(LoanMember, related_name='credit_histories', on_delete=models.PROTECT)
    point = models.IntegerField()


class Loan(TimestampedModel):
    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'

    application = models.ForeignKey(LoanApplication, related_name='application_loans', on_delete=models.PROTECT)
    loan_applicant = models.ForeignKey(LoanMemberApplication, related_name='applicant_loans', on_delete=models.PROTECT)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=LOAN_STATUS, default=LOAN_STATUS.active)


class LoanPayment(TimestampedModel):
    class Meta:
        verbose_name = 'Loan Payment'
        verbose_name_plural = 'Loan Payments'

    loan_applicant = models.ForeignKey(LoanMemberApplication, related_name='applicant_payments',
                                       on_delete=models.PROTECT)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2)
    original_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_amount = models.DecimalField(max_digits=12, decimal_places=2)
    fee = models.DecimalField(max_digits=12, decimal_places=2)


class LoanTerm(TimestampedModel):
    class Meta:
        verbose_name = 'Loan Term'
        verbose_name_plural = 'Loan Terms'

    loan_applicant = models.ForeignKey(LoanMemberApplication, related_name='applicant_terms',
                                       on_delete=models.PROTECT)
    original_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    pay_date = models.DateTimeField(help_text='The date member should pay the loan')
    paid_date = models.DateTimeField(help_text='The date member paid the loan', null=True)
    paid_status = models.CharField(max_length=50, choices=LOAN_TERM_STATUS, null=True)
    paid = models.BooleanField(default=False)
    payment = models.ForeignKey(LoanPayment, related_name='loan_payment_terms', null=True, on_delete=models.PROTECT)


class LoanTermNotification(TimestampedModel):
    loan_term = models.ForeignKey(LoanTerm, related_name='loan_term_notifications', on_delete=models.CASCADE)
    notification_status = models.CharField(max_length=50, choices=LOAN_TERM_NOTIFICATION_STATUS,
                                           default=LOAN_TERM_NOTIFICATION_STATUS.not_yet)
    notification_note = models.TextField(null=True, blank=True)
