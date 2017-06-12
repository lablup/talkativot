from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^user/(?P<user_id>[^/]+)$', views.ConversationView.as_view())
]
