from loan.models import Loan


# Extend class to do business of model
class LoanBusiness(Loan):
    class Meta:
        proxy = True
    pass
