from django.urls import path, include
from rest_framework.routers import DefaultRouter

from loan_admin.resource import LoanApplicationViewSet, LoanTermViewSet, LoanTermNotificationViewSet

router = DefaultRouter()
router.register('loan-applications', LoanApplicationViewSet)
router.register('loan-terms', LoanTermViewSet)
router.register('loan-term-notifications', LoanTermNotificationViewSet)

patterns = ([
    path('', include(router.urls)),
], 'loan-admin')

urlpatterns = [
    path('admin/', include(patterns)),
]
