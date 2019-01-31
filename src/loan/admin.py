from django.contrib import admin

from loan.models import LoanProgram, LoanMember, LoanApplication, LoanMemberApplication, Loan, LoanPayment, \
    LoanMemberApplicationDataField, LoanTerm


@admin.register(LoanProgram)
class LoanProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'rate', 'active']


@admin.register(LoanMember)
class LoanMemberAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'user_id', 'user_name', 'user_phone', 'phone_verification_code']


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['program', 'loan_amount', 'rate', 'cycle', 'term', 'status', 'note']


class LoanMemberApplicationDataFieldInline(admin.StackedInline):
    model = LoanMemberApplicationDataField
    list_display = ('field_name', 'field_value')
    extra = 1


class LoanInline(admin.StackedInline):
    model = Loan
    list_display = ('loan_amount', 'start_date', 'end_date', 'status')
    extra = 1


class LoanTermInline(admin.StackedInline):
    model = LoanTerm
    list_display = ('total_amount', 'original_amount', 'interest_amount',
                    'pay_date', 'paid_date', 'paid', 'paid_status')
    extra = 1


class LoanPaymentInline(admin.StackedInline):
    model = LoanPayment
    list_display = ('paid_amount', 'original_amount', 'interest_amount', 'status')
    extra = 1


@admin.register(LoanMemberApplication)
class LoanMemberApplicationAdmin(admin.ModelAdmin):
    list_display = ['application', 'member', 'main', 'status', 'active']
    search_fields = ['member__user_email', 'member__user_phone', ]
    inlines = (LoanMemberApplicationDataFieldInline,
               LoanInline,
               LoanTermInline,
               LoanPaymentInline)
