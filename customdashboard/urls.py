from .views import DefaultCustomDashboard, PublicDashboard, ProgramList, InternalDashboard

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

                       #rimma
                       url(r'^rrima/$', 'customdashboard.views.RRIMAPublicDashboard', name='rrima_public_dashboard'),

                       #jupyternotebooks (For RIMMA now but could be used for any program as well)
                       url(r'^notebook/(?P<id>\w+)/$', 'customdashboard.views.Notebook', name='notebook'),

                       #display default custom dashboard
                       url(r'^(?P<id>\w+)/$', 'customdashboard.views.DefaultCustomDashboard', name='default_custom_dashboard'),
                       url(r'^(?P<id>\w+)/([0-9]+)/$', 'customdashboard.views.DefaultCustomDashboard', name='default_custom_dashboard'),

                       #project status
                       url(r'^(?P<id>[0-9]+)/(?P<status>[\w ]+)/$', 'customdashboard.views.DefaultCustomDashboard', name='project_status'),

                       #gallery
                       url(r'^public/(?P<id>\w+)/gallery/([0-9]+)/$', 'customdashboard.views.Gallery', name='gallery'),
                       url(r'^public/(?P<id>\w+)/([0-9]+)/gallery/([0-9]+)/$', 'customdashboard.views.Gallery', name='gallery'),
                       )


