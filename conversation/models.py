# System modules
import os
import uuid

# Django modules
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.core.cache import cache
from django.utils import timezone


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="conversation")
