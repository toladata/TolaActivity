from django.conf.urls import patterns, include, url

from .views import CollectedDataList, CollectedDataCreate, CollectedDataUpdate, CollectedDataDelete, IndicatorCreate, IndicatorDelete, IndicatorUpdate,\
    IndicatorList, IndicatorExport, IndicatorReportData,CollectedDataReportData, IndicatorReport, IndicatorDataExport, TVAReport, DisaggregationReport, PeriodicTargetDeleteView


urlpatterns = [

    # INDICATOR PLANING TOOL
    # Home
    url(r'^home/(?P<program>\w+)/(?P<indicator>\w+)/(?P<type>\w+)/$', IndicatorList.as_view(), name='indicator_list'),

    # Indicator Form
    url(r'^indicator_list/(?P<pk>\w+)/$', IndicatorList.as_view(), name='indicator_list'),
    url(r'^indicator_create/(?P<id>\w+)/$', 'indicators.views.indicator_create', name='indicator_create'),
    url(r'^indicator_add/(?P<id>\w+)/$', IndicatorCreate.as_view(), name='indicator_add'),
    url(r'^indicator_update/(?P<pk>\w+)/$', IndicatorUpdate.as_view(), name='indicator_update'),
    url(r'^indicator_delete/(?P<pk>\w+)/$', IndicatorDelete.as_view(), name='indicator_delete'),

    url(r'^periodic_target_delete/(?P<pk>\w+)/$', PeriodicTargetDeleteView.as_view(), name='pt_delete'),

    # Collected Data List
    url(r'^collecteddata/(?P<program>\w+)/(?P<indicator>\w+)/(?P<type>\w+)/$', CollectedDataList.as_view(), name='collecteddata_list'),
    url(r'^collecteddata_add/(?P<program>\w+)/(?P<indicator>\w+)/$', CollectedDataCreate.as_view(), name='collecteddata_add'),
    url(r'^collecteddata_import/$', 'indicators.views.collecteddata_import', name='collecteddata_import'),
    url(r'^collecteddata_update/(?P<pk>\w+)/$', CollectedDataUpdate.as_view(), name='collecteddata_update'),
    url(r'^collecteddata_delete/(?P<pk>\w+)/$', CollectedDataDelete.as_view(), name='collecteddata_delete'),
    url(r'^collecteddata_export/(?P<program>\w+)/(?P<indicator>\w+)/$', CollectedDataList.as_view(), name='collecteddata_list'),

    # Indicator Report
    url(r'^report/(?P<program>\w+)/(?P<indicator>\w+)/(?P<type>\w+)/$', 'indicators.views.indicator_report', name='indicator_report'),
    url(r'^tvareport/$', TVAReport.as_view(), name='tvareport'),
    url(r'^disrep/(?P<program>\w+)/$', DisaggregationReport.as_view(), name='disrep'),
    url(r'^report_table/(?P<program>\w+)/(?P<indicator>\w+)/(?P<type>\w+)/$', IndicatorReport.as_view(), name='indicator_table'),
    url(r'^program_report/(?P<program>\w+)/$', 'indicators.views.programIndicatorReport',name='programIndicatorReport'),

    # Indicator Data Report
    url(r'^data/(?P<id>\w+)/(?P<program>\w+)/(?P<type>\w+)/$', 'indicators.views.indicator_data_report', name='indicator_data_report'),
    url(r'^data/(?P<id>\w+)/(?P<program>\w+)/(?P<type>\w+)/map/$', 'indicators.views.indicator_data_report', name='indicator_data_report'),
    url(r'^data/(?P<id>\w+)/(?P<program>\w+)/(?P<type>\w+)/graph/$', 'indicators.views.indicator_data_report', name='indicator_data_report'),
    url(r'^data/(?P<id>\w+)/(?P<program>\w+)/(?P<type>\w+)/table/$', 'indicators.views.indicator_data_report', name='indicator_data_report'),
    url(r'^data/(?P<id>\w+)/(?P<program>\w+)/$', 'indicators.views.indicator_data_report', name='indicator_data_report'),
    url(r'^data/(?P<id>\w+)/$', 'indicators.views.indicator_data_report', name='indicator_data_report'),
    url(r'^export/(?P<id>\w+)/(?P<program>\w+)/(?P<indicator_type>\w+)/$', IndicatorExport.as_view(), name='indicator_export'),

    # ajax calls
    url(r'^service/(?P<service>[-\w]+)/service_json/', 'indicators.views.service_json', name='service_json'),
    url(r'^collected_data_table/(?P<indicator>[-\w]+)/(?P<program>[-\w]+)/', 'indicators.views.collected_data_json', name='collected_data_json'),
    url(r'^program_indicators/(?P<program>[-\w]+)/(?P<indicator>[-\w]+)/(?P<type>[-\w]+)', 'indicators.views.program_indicators_json', name='program_indicators_json'),
    url(r'^report_data/(?P<id>\w+)/(?P<program>\w+)/(?P<type>\w+)/$', IndicatorReportData.as_view(),name='indicator_report_data'),
    url(r'^report_data/(?P<id>\w+)/(?P<program>\w+)/(?P<indicator_type>\w+)/export/$', IndicatorExport.as_view(),name='indicator_export'),
    url(r'^collecteddata_report_data/(?P<program>\w+)/(?P<indicator>\w+)/(?P<type>\w+)/$', CollectedDataReportData.as_view(), name='collecteddata_report_data'),
    url(r'^collecteddata_report_data/(?P<program>\w+)/(?P<indicator>\w+)/(?P<type>\w+)/export/$', IndicatorDataExport.as_view(), name='collecteddata_report_data'),


]