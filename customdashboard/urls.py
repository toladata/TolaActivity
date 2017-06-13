from .views import *
from customdashboard import views as customdashboardviews
from django.conf.urls import *


# place app url patterns here

urlpatterns = [

                       #display public custom dashboard
                       url(r'^program_list/(?P<pk>\w+)/$', ProgramList.as_view(), name='program_list'),
                       url(r'^program_dashboard/(?P<id>\w+)/(?P<public>\w+)/$', customdashboardviews.PublicDashboard, name='public_dashboard'),
                       url(r'^public/(?P<id>\w+)/$', customdashboardviews.PublicDashboard, name='public_dashboard'),
                       url(r'^public/(?P<id>\w+)/([0-9]+)/$', customdashboardviews.PublicDashboard, name='public_dashboard'),

                       #Extermely custom dashboards
                       url(r'^survey_public/$', customdashboardviews.SurveyPublicDashboard, name='survey_public_dashboard'),
                       url(r'^survey_talk_public/$', customdashboardviews.SurveyTalkPublicDashboard, name='survey_talk_public_dashboard'),

                       #rimma
                       url(r'^rrima/$', customdashboardviews.RRIMAPublicDashboard, name='rrima_public_dashboard'),

                       #jupyternotebooks (For RIMMA now but could be used for any program as well)
                       url(r'^notebook/(?P<id>\w+)/$', customdashboardviews.Notebook, name='notebook'),

                       #display default custom dashboard
                       url(r'^(?P<id>\w+)/$', customdashboardviews.DefaultCustomDashboard, name='default_custom_dashboard'),
                       url(r'^(?P<id>\w+)/([0-9]+)/$', customdashboardviews.DefaultCustomDashboard, name='default_custom_dashboard'),

                       #project status
                       url(r'^(?P<id>[0-9]+)/(?P<status>[\w ]+)/$', customdashboardviews.DefaultCustomDashboard, name='project_status'),

]
