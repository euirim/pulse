"""pulse URL Configuration

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
import os

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers

from records.views import RecordViewSet
from keyphrases.views import KeyphraseViewSet

router = routers.DefaultRouter()
router.register(r'records', RecordViewSet, basename='record')
router.register(r'keyphrases', KeyphraseViewSet, basename='keyphrase')

urlpatterns = [
    path('clausewitz-wsj/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-browser/', include('rest_framework.urls'))
]

if os.environ["PULSE_HOST_TYPE"] == "dev":
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)