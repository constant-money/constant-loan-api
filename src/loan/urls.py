from django.urls import path, include
from rest_framework.routers import DefaultRouter

from loan.views import SampleAuthView, PhoneVerificationView, LoanApplicationView

router = DefaultRouter()

patterns = ([
    path('', include(router.urls)),
    path('sample-auth/', SampleAuthView.as_view(), name='sample-auth-view'),
    path('phone-verification/', PhoneVerificationView.as_view(), name='phone-verification-view'),
    path('loan-application/', LoanApplicationView.as_view(), name='loan-application-view'),
], 'loan')

urlpatterns = [
    path('loan/', include(patterns)),
]
