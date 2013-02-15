from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# URIs for user-specific views and pages
# These are included in the main url patterns with a "/users/" prefix
# Main URIs
urlpatterns = patterns('the_design_exchange.views',
    url(r'^', include('design_methods.urls')),
)
