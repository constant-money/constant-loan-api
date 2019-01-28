from django.urls import path, include
from rest_framework.routers import DefaultRouter

from loan.views import SampleAuthView

router = DefaultRouter()

patterns = ([
    path('', include(router.urls)),
    path('sample-auth/', SampleAuthView.as_view(), name='sample-auth-view'),
], 'loan')

urlpatterns = [
    path('loan/', include(patterns)),
]
