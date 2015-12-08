from django.conf.urls import patterns, include, url

from .views import CollectedDataList, CollectedDataCreate, CollectedDataUpdate, CollectedDataDelete, IndicatorCreate, IndicatorDelete, IndicatorUpdate,\
    IndicatorList


urlpatterns = patterns('',

    ###INDICATOR PLANING TOOL
    #Home
    url(r'^home/(?P<pk>\w+)/$', IndicatorList.as_view(), name='indicator_list'),

    #Indicator Report
    url(r'^report/(?P<program>\w+)/$', 'indicators.views.indicator_report', name='indicator_report'),
    url(r'^program_report/(?P<program>\w+)/$', 'indicators.views.programIndicatorReport', name='programIndicatorReport'),

    #Indicator Form
    url(r'^indicator_list/(?P<pk>\w+)/$', IndicatorList.as_view(), name='indicator_list'),
    url(r'^indicator_create/(?P<id>\w+)/$', 'indicators.views.indicator_create', name='indicator_create'),
    url(r'^indicator_add/(?P<id>\w+)/$', IndicatorCreate.as_view(), name='indicator_add'),
    url(r'^indicator_update/(?P<pk>\w+)/$', IndicatorUpdate.as_view(), name='indicator_update'),
    url(r'^indicator_delete/(?P<pk>\w+)/$', IndicatorDelete.as_view(), name='indicator_delete'),

    #Collected Data List
    url(r'^collecteddata/(?P<indicator>\w+)/$', CollectedDataList.as_view(), name='collecteddata_list'),
    url(r'^collecteddata/(?P<indicator>\w+)/(?P<program>\w+)/$', CollectedDataList.as_view(), name='collecteddata_list'),
    url(r'^collecteddata/(?P<indicator>\w+)/(?P<program>\w+)/(?P<agreement>\w+)/$', CollectedDataList.as_view(), name='collecteddata_list'),

    url(r'^collecteddata_add/(?P<agreement>\w+)/$', CollectedDataCreate.as_view(), name='collecteddata_add'),
    url(r'^collecteddata_add/(?P<program>\w+)/(?P<indicator>\w+)/$', CollectedDataCreate.as_view(), name='collecteddata_add'),
    url(r'^collecteddata_update/(?P<pk>\w+)/$', CollectedDataUpdate.as_view(), name='collecteddata_update'),
    url(r'^collecteddata_delete/(?P<pk>\w+)/$', CollectedDataDelete.as_view(), name='collecteddata_delete'),

    #Indicator Data Report
    url(r'^data/(?P<id>\w+)/$', 'indicators.views.indicator_data_report', name='indicator_data_report'),
    url(r'^data/(?P<id>\w+)/(?P<program>\w+)/map/$', 'indicators.views.indicator_data_report', name='indicator_data_report'),
    url(r'^data/(?P<id>\w+)/(?P<program>\w+)/graph/$', 'indicators.views.indicator_data_report', name='indicator_data_report'),
    url(r'^data/(?P<id>\w+)/(?P<program>\w+)/table/$', 'indicators.views.indicator_data_report', name='indicator_data_report'),
    url(r'^data/(?P<id>\w+)/(?P<program>\w+)/$', 'indicators.views.indicator_data_report', name='indicator_data_report'),

    #ajax calls
    url(r'^service/(?P<service>[-\w]+)/service_json/', 'indicators.views.service_json', name='service_json'),

)