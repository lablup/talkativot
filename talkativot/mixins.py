"""
Mixin for talkativot
"""
import json

from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.views.generic.base import ContextMixin
from django.views.generic.detail import SingleObjectMixin


class AjaxFormResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        if self.request.is_ajax():
            result = json.loads(form.errors.as_json())
            return JsonResponse(result, safe=False)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return HttpResponseRedirect(self.get_success_url())


class JsonResponseMixin:
    '''
    Reference:
    https://docs.djangoproject.com/en/1.10/topics/class-based-views/mixins/#jsonresponsemixin-example
    '''

    context_json_filter = None

    def get_json_data(self, context):
        '''
        Default implementation: remove some auto-injected but not
        JSON-serializable context variables.
        If self.context_json_filter is set to a collection such as list or
        set, then it instead preserves only the key-value pairs whose key is
        in the filter.

        You may override this method to implement your own serialization and
        context filtering process.
        '''
        if self.context_json_filter is None:
            if isinstance(self, SingleObjectMixin):
                name = self.get_context_object_name(self.object)
                if name in context: del context[name]
                if 'object' in context: del context['object']
            if isinstance(self, ContextMixin):
                if 'view' in context: del context['view']
            return context
        else:
            return {k: v for k, v in context.items()
                    if k in self.context_json_filter}

    def render_to_response(self, context, **response_kwargs):
        '''
        If the request is an AJAX call, then call self.get_json_data() for
        context-to-JSON conversion.
        Otherwise, just call the base method transparently.
        '''
        if self.request.is_ajax():
            data = self.get_json_data(context)
            return JsonResponse(data, **response_kwargs)
        else:
            return super().render_to_response(context, **response_kwargs)
