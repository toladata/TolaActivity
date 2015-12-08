from .views import DefaultCustomDashboard

from django.conf.urls import *

# place app url patterns here

urlpatterns = patterns('',
                       #display default custom dashboard
                       url(r'^$', 'customdashboard.views.DefaultCustomDashboard', name='default_custom_dashboard'),
                       url(r'^(?P<id>\w+)/$', 'customdashboard.views.DefaultCustomDashboard', name='default_custom_dashboard'),
                       url(r'^(?P<id>\w+)/([0-9]+)/$', 'customdashboard.views.DefaultCustomDashboard', name='default_custom_dashboard'),
                        #project status
                        url(r'^(?P<id>[0-9]+)/(?P<status>[\w ]+)/$', 'customdashboard.views.DefaultCustomDashboard', name='project_status'),


                       )
