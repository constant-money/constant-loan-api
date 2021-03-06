from decimal import Decimal

import factory

from common.business import get_now
from loan.constants import LOAN_APPLICATION_STATUS, LOAN_TERM_STATUS


class LoanProgramFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'loan.LoanProgram'

    name = factory.Sequence(lambda n: "LoanProgram-%03d" % n)
    min_loan_amount = Decimal(10)
    max_loan_amount = Decimal(100)
    min_member = 3
    max_member = 3
    rate = Decimal('1.5')
    cycle = 7


class LoanMemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'loan.LoanMember'

    user_id = factory.Sequence(lambda n: n)


class LoanApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'loan.LoanApplication'

    program = factory.SubFactory(LoanProgramFactory)
    loan_amount = Decimal(10)
    member_required = 3
    member_allowed = 1
    rate = Decimal('1.5')
    cycle = 7
    term = 6
    status = factory.Iterator([item[0] for item in LOAN_APPLICATION_STATUS])


class LoanMemberApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'loan.LoanMemberApplication'

    application = factory.SubFactory(LoanApplicationFactory)
    member = factory.SubFactory(LoanMemberFactory)


class LoanMemberApplicationDataFieldFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'loan.LoanMemberApplicationDataField'

    loan_applicant = factory.SubFactory(LoanMemberApplicationFactory)


class MemberCreditHistoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'loan.MemberCreditHistory'

    member = factory.SubFactory(LoanMemberFactory)


class LoanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'loan.Loan'

    application = factory.SubFactory(LoanApplicationFactory)
    loan_applicant = factory.SubFactory(LoanMemberApplicationFactory)


class LoanTermFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'loan.LoanTerm'

    loan_applicant = factory.SubFactory(LoanMemberApplicationFactory)
    original_amount = Decimal('10')
    interest_amount = Decimal('0.15')
    total_amount = Decimal('10.15')
    pay_date = get_now()
    paid_status = factory.Iterator([item[0] for item in LOAN_TERM_STATUS])


class LoanPaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'loan.LoanPayment'

    loan_applicant = factory.SubFactory(LoanMemberApplicationFactory)


class LoanTermNotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'loan.LoanTermNotification'

    loan_term = factory.SubFactory(LoanTermFactory)
