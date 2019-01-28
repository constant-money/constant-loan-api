from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

patterns = ([
    path('', include(router.urls)),
], 'loan-admin')

urlpatterns = [
    path('admin/', include(patterns)),
]
