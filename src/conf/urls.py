"""coin_exchange URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from loan.views import StartView

urlpatterns = [
    path('', StartView.as_view()),
    path('loan-api/__admin/', admin.site.urls),
    path('loan-api/', StartView.as_view()),
    path('loan-api/', include('loan.urls')),
    path('loan-api/', include('loan_admin.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
