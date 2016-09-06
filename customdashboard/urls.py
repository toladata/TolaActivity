from .views import DefaultCustomDashboard, PublicDashboard, ProgramList, InternalDashboard, Gallery

from django.conf.urls import *


# place app url patterns here

urlpatterns = patterns('',


                       #display public custom dashboard
                       url(r'^program_list/(?P<pk>\w+)/$', ProgramList.as_view(), name='program_list'),
                       url(r'^internal_dashboard/(?P<pk>\w+)/$', InternalDashboard.as_view(), name='internal_dashboard'),
                       url(r'^survey_public/report$', 'customdashboard.views.ReportPublicDashboard', name='report_public_dashboard'),
                       url(r'^survey_public/$', 'customdashboard.views.SurveyPublicDashboard', name='survey_public_dashboard'),
                       url(r'^survey_talk_public/$', 'customdashboard.views.SurveyTalkPublicDashboard', name='survey_talk_public_dashboard'),
                       url(r'^public/(?P<id>\w+)/$', 'customdashboard.views.PublicDashboard', name='public_dashboard'),
                       url(r'^public/(?P<id>\w+)/([0-9]+)/$', 'customdashboard.views.PublicDashboard', name='public_dashboard'),

                       #display default custom dashboard
                       url(r'^(?P<id>\w+)/$', 'customdashboard.views.DefaultCustomDashboard', name='default_custom_dashboard'),
                       url(r'^(?P<id>\w+)/([0-9]+)/$', 'customdashboard.views.DefaultCustomDashboard', name='default_custom_dashboard'),

                       #project status
                       url(r'^(?P<id>[0-9]+)/(?P<status>[\w ]+)/$', 'customdashboard.views.DefaultCustomDashboard', name='project_status'),

                       #gallery
                       url(r'^public/(?P<id>\w+)/gallery/([0-9]+)/$', 'customdashboard.views.Gallery', name='gallery'),

                       #dashboard schemes
                       url(r'^(?P<id>[0-9]+)/data/public/$', 'customdashboard.views.AnalyticsDashboard', name='analytics_custom_dashboard'),
                       url(r'^(?P<id>[0-9]+)/text/public/$', 'customdashboard.views.NarrativeDashboard', name='text_custom_dashboard'),
                       url(r'^(?P<id>[0-9]+)/map/public/$', 'customdashboard.views.MapDashboard', name='map_custom_dashboard'),
                       # url(r'^jupyter/1/$', 'customdashboard.views.RRIMAJupyterView1', name='jupyter_dashboard'),                          
)
