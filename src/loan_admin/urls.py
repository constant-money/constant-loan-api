from django.urls import path, include
from rest_framework.routers import DefaultRouter

from loan_admin.resource import LoanApplicationViewSet

router = DefaultRouter()
router.register('loan-applications', LoanApplicationViewSet)

patterns = ([
    path('', include(router.urls)),
], 'loan-admin')

urlpatterns = [
    path('admin/', include(patterns)),
]
