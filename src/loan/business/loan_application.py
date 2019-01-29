from loan.constants import LOAN_APPLICATION_STATUS
from loan.models import LoanApplication


# Extend class to do business of model
class LoanApplicationBusiness(LoanApplication):
    class Meta:
        proxy = True

    def approve(self):
        self.status = LOAN_APPLICATION_STATUS.approved
        self.save()

    def reject(self, note=''):
        self.status = LOAN_APPLICATION_STATUS.rejected
        self.note = note
        self.save()
