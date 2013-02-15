from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView, CreateView
from design_methods.views import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# URIs for user-specific views and pages
# These are included in the main url patterns with a "/users/" prefix
user_urlpatterns = patterns('design_methods.views',
    url(r'^$', UserList.as_view()),
    url(r'^(?P<pk>\d+)/$', UserDetails.as_view(), name='user_details'),
    url(r'^new/$', Register.as_view(), name="register"),
)

# URIs for messages
# TODO message lists, details, and replies
message_urlpatterns = patterns('design_methods.views',
    url(r'^$', 'list_messages'),
    url(r'^new/$', 'send_message'),
)

# URIs for methods
method_urlpatterns = patterns('design_methods.views',
    url(r'^$', 'list_methods'),
    url(r'^new/$', 'create_method'),
    url(r'^(?P<pk>\d+)/$', MethodDetails.as_view(), name='method_details'),
)

# Main URIs
urlpatterns = patterns('design_methods.views',
    url(r'^$', 'home', name='home'),
    url(r'^users/', include(user_urlpatterns)),
    url(r'^login/', login, {'template_name': 'sessions/login.html'}),
    url(r'^logout/', logout, {'next_page': '/'}),
    url(r'^messages/', include(message_urlpatterns)),
    url(r'^methods/', include(method_urlpatterns)),
)
