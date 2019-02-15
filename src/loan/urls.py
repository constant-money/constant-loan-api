from django.urls import path, include
from rest_framework.routers import DefaultRouter

from loan.resource import LoanApplicationViewSet, LoanTermViewSet, LoanProgramViewSet
from loan.views import SampleAuthView, PhoneVerificationView, LoanApplicationView, LoanConnectView, \
    LoanTermReminderView, LoanTermAutoPayView, LoanApplicationConnectionReminderView, LoanApplicationExpiredView, \
    LoanDisconnectView, LoanApplicationCheckView

router = DefaultRouter()
router.register('loan-programs', LoanProgramViewSet)
router.register('loan-applications', LoanApplicationViewSet)
router.register('loan-terms', LoanTermViewSet)

patterns = ([
    path('', include(router.urls)),
    path('sample-auth/', SampleAuthView.as_view(), name='sample-auth-view'),
    path('phone-verification/', PhoneVerificationView.as_view(), name='phone-verification-view'),
    path('loan-application/', LoanApplicationView.as_view(), name='loan-application-view'),
    path('loan-application/check/', LoanApplicationCheckView.as_view(), name='loan-application-check-view'),
    path('loan-connect/', LoanConnectView.as_view(), name='loan-connect-view'),
    path('loan-disconnect/', LoanDisconnectView.as_view(), name='loan-disconnect-view'),
    path('loan-term-reminder/', LoanTermReminderView.as_view(), name='loan-term-reminder-view'),
    path('loan-term-autopay/', LoanTermAutoPayView.as_view(), name='loan-term-autopay-view'),
    path('loan-application-connnecion-reminder/', LoanApplicationConnectionReminderView.as_view(),
         name='loan-application-connection-reminder'),
    path('loan-application-expired/', LoanApplicationExpiredView.as_view(),
         name='loan-application-connection-reminder'),
], 'loan')

urlpatterns = [
    path('loan/', include(patterns)),
]
