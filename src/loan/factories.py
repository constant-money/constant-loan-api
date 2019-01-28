import factory


class LoanProgramFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'loan.LoanProgram'


class LoanMemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'loan.LoanMember'


class LoanApplicationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'loan.LoanApplication'

    program = factory.SubFactory(LoanProgramFactory)


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


class LoanPaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'loan.LoanPayment'

    loan_applicant = factory.SubFactory(LoanMemberApplicationFactory)
