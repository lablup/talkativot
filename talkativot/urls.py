"""talkativot URL Configuration
"""
import logging

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

log = logging.getLogger('talkativot.urls')

urlpatterns = [
    url(r'^conversation/', include('conversation.urls', namespace="conversation")),
]
