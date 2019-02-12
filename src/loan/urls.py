from django.urls import path, include
from rest_framework.routers import DefaultRouter

from loan.resource import LoanApplicationViewSet, LoanTermViewSet, LoanProgramViewSet
from loan.views import SampleAuthView, PhoneVerificationView, LoanApplicationView, LoanConnectView

router = DefaultRouter()
router.register('loan-programs', LoanProgramViewSet)
router.register('loan-applications', LoanApplicationViewSet)
router.register('loan-terms', LoanTermViewSet)

patterns = ([
    path('', include(router.urls)),
    path('sample-auth/', SampleAuthView.as_view(), name='sample-auth-view'),
    path('phone-verification/', PhoneVerificationView.as_view(), name='phone-verification-view'),
    path('loan-application/', LoanApplicationView.as_view(), name='loan-application-view'),
    path('loan-connect/', LoanConnectView.as_view(), name='loan-connect-view'),
], 'loan')

urlpatterns = [
    path('loan/', include(patterns)),
]
