"""
Super-simple bot engine test
"""
# System modules
import base64
import copy as cp
import datetime
from datetime import timedelta
import json
import logging
import markdown
import os
import random
import time
import uuid

# Django modules
from django.apps import apps
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.exceptions import ValidationError, ObjectDoesNotExist, SuspiciousOperation
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import escape
from django.utils.translation import ugettext as _
from django.views.generic.base import View, TemplateView
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.sites.shortcuts import get_current_site

from conversation.forms import ConversationForm
from talkativot.mixins import AjaxFormResponseMixin, JsonResponseMixin
from conversation.models import Conversation


class ConversationView(AjaxFormResponseMixin, CreateView):
    """ Handles conversation I/O.
    """

    model = Conversation
    object = None

    def __init__(self):
        super().__init__()
        import logging
        self.logger = logging.getLogger('talkativot')
        self.logger.info('\n\n##### Test logging started (devs.)')

    def get_object(self, queryset=None):
        self.user_id = self.kwargs['user_id']
        data = json.loads(request.body.decode('utf-8'))
        try:
            obj = None # Dummy for now
        except ObjectDoesNotExist:
            raise
        return obj

    def create_object(self, context):
        object = None # Dummy for now
        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['kind'] = 'conversation'
        return context

    def post(self, request, *args, **kwargs):
        form = ConversationForm(json.loads(request.body.decode('utf-8')))
        result = {
            "success": 1,
            "message": "test"
        }
        return JsonResponse(result)
