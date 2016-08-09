from .views import *

from django.conf.urls import *

# place app url patterns here

urlpatterns = [
                       ###activitydb
                       url(r'^dashboard/project/(?P<pk>\w+)/$', ProjectDash.as_view(), name='project_dashboard'),
                       url(r'^dashboard/project/(?P<pk>\w+)$', ProjectDash.as_view(), name='project_dashboard'),
                       url(r'^dashboard/project', ProjectDash.as_view(), name='project_dashboard'),
                       url(r'^dashboard/(?P<pk>\w+)/(?P<status>\w+)/$', ProgramDash.as_view(), name='dashboard'),
                       url(r'^dashboard/(?P<pk>\w+)/$', ProgramDash.as_view(), name='dashboard'),

                       url(r'^projectagreement_list/(?P<pk>\w+)/$', ProjectAgreementList.as_view(), name='projectagreement_list'),
                       url(r'^projectagreement_add/$', ProjectAgreementCreate.as_view(), name='projectagreement_add'),
                       url(r'^projectagreement_update/(?P<pk>\w+)/$', ProjectAgreementUpdate.as_view(), name='projectagreement_update'),
                       url(r'^projectagreement_delete/(?P<pk>\w+)/$', ProjectAgreementDelete.as_view(), name='projectagreement_delete'),
                       url(r'^projectagreement_import', ProjectAgreementImport.as_view(), name='projectagreement_import'),
                       url(r'^projectagreement_detail/(?P<pk>\w+)/$', ProjectAgreementDetail.as_view(), name='projectagreement_detail'),

                       url(r'^projectcomplete_list/(?P<pk>\w+)/$', ProjectCompleteList.as_view(), name='projectcomplete_list'),
                       url(r'^projectcomplete_add/(?P<pk>\w+)/$', ProjectCompleteCreate.as_view(), name='projectcomplete_add'),
                       url(r'^projectcomplete_update/(?P<pk>\w+)/$', ProjectCompleteUpdate.as_view(), name='projectcomplete_update'),
                       url(r'^projectcomplete_delete/(?P<pk>\w+)/$', ProjectCompleteDelete.as_view(), name='projectcomplete_delete'),
                       url(r'^projectcomplete_import', ProjectCompleteImport.as_view(), name='projectcomplete_import'),
                       url(r'^projectcomplete_detail/(?P<pk>\w+)/$', ProjectCompleteDetail.as_view(), name='projectcomplete_detail'),

                       url(r'^siteprofile_list/(?P<program_id>\w+)/(?P<activity_id>\w+)/$', SiteProfileList.as_view(), name='siteprofile_list'),
                       url(r'^siteprofile_report/(?P<pk>\w+)/$', SiteProfileReport.as_view(), name='siteprofile_report'),
                       url(r'^siteprofile_add', SiteProfileCreate.as_view(), name='siteprofile_add'),
                       url(r'^siteprofile_update/(?P<pk>\w+)/$', SiteProfileUpdate.as_view(), name='siteprofile_update'),
                       url(r'^siteprofile_delete/(?P<pk>\w+)/$', SiteProfileDelete.as_view(), name='siteprofile_delete'),

                       url(r'^documentation_list/(?P<program>\w+)/(?P<project>\w+)/$', DocumentationList.as_view(), name='documentation_list'),
                       url(r'^documentation_add', DocumentationCreate.as_view(), name='documentation_add'),
                       url(r'^documentation_agreement_list/(?P<program>\w+)/(?P<project>\w+)/$', DocumentationAgreementList.as_view(), name='documentation_agreement_list'),
                       url(r'^documentation_agreement_add/(?P<id>\w+)/$', DocumentationAgreementCreate.as_view(),name='documentation_agreement_add'),
                       url(r'^documentation_agreement_update/(?P<pk>\w+)/(?P<id>\w+)/$', DocumentationAgreementUpdate.as_view(), name='documentation_agreement_update'),
                       url(r'^documentation_agreement_delete/(?P<pk>\w+)/$', DocumentationAgreementDelete.as_view(), name='documentation_agreement_delete'),
                       url(r'^documentation_update/(?P<pk>\w+)/$', DocumentationUpdate.as_view(), name='documentation_update'),
                       url(r'^documentation_delete/(?P<pk>\w+)/$', DocumentationDelete.as_view(), name='documentation_delete'),

                       url(r'^monitor_list/(?P<pk>\w+)/$', MonitorList.as_view(), name='monitor_list'),
                       url(r'^monitor_add/(?P<id>\w+)/$', MonitorCreate.as_view(), name='monitor_add'),
                       url(r'^monitor_update/(?P<pk>\w+)/$', MonitorUpdate.as_view(), name='monitor_update'),
                       url(r'^monitor_delete/(?P<pk>\w+)/$', MonitorDelete.as_view(), name='monitor_delete'),

                       url(r'^quantitative_add/(?P<id>\w+)/$', QuantitativeOutputsCreate.as_view(), name='quantitative_add'),
                       url(r'^quantitative_update/(?P<pk>\w+)/$', QuantitativeOutputsUpdate.as_view(), name='quantitative_update'),
                       url(r'^quantitative_delete/(?P<pk>\w+)/$', QuantitativeOutputsDelete.as_view(), name='quantitative_delete'),

                       url(r'^benchmark_add/(?P<id>\w+)/$', BenchmarkCreate.as_view(), name='benchmark_add'),
                       url(r'^benchmark_update/(?P<pk>\w+)/$', BenchmarkUpdate.as_view(), name='benchmark_update'),
                       url(r'^benchmark_delete/(?P<pk>\w+)/$', BenchmarkDelete.as_view(), name='benchmark_delete'),

                       # urls for projectcomplete version of popup
                       url(r'^benchmark_complete_add/(?P<id>\w+)/$', BenchmarkCreate.as_view(), name='benchmark_add'),
                       url(r'^benchmark_complete_update/(?P<pk>\w+)/$', BenchmarkUpdate.as_view(), name='benchmark_update'),
                       url(r'^benchmark_complete_delete/(?P<pk>\w+)/$', BenchmarkDelete.as_view(), name='benchmark_delete'),

                       url(r'^training_list/(?P<pk>\w+)/$', TrainingList.as_view(), name='training_list'),
                       url(r'^training_add/(?P<id>\w+)/$', TrainingCreate.as_view(), name='training_add'),
                       url(r'^training_update/(?P<pk>\w+)/$', TrainingUpdate.as_view(), name='training_update'),
                       url(r'^training_delete/(?P<pk>\w+)/$', TrainingDelete.as_view(), name='training_delete'),

                       url(r'^stakeholder_list/(?P<pk>\w+)/$', StakeholderList.as_view(), name='stakeholder_list'),
                       url(r'^stakeholder_add/(?P<id>\w+)/$', StakeholderCreate.as_view(), name='stakeholder_add'),
                       url(r'^stakeholder_update/(?P<pk>\w+)/$', StakeholderUpdate.as_view(), name='stakeholder_update'),
                       url(r'^stakeholder_delete/(?P<pk>\w+)/$', StakeholderDelete.as_view(), name='stakeholder_delete'),

                       url(r'^contact_list/(?P<pk>\w+)/$', ContactList.as_view(), name='contact_list'),
                       url(r'^contact_add/(?P<id>\w+)/$', ContactCreate.as_view(), name='contact_add'),
                       url(r'^contact_update/(?P<pk>\w+)/$', ContactUpdate.as_view(), name='contact_update'),
                       url(r'^contact_delete/(?P<pk>\w+)/$', ContactDelete.as_view(), name='contact_delete'),

                       url(r'^checklistitem_list/(?P<pk>\w+)/$', ChecklistItemList.as_view(), name='checklistitem_list'),
                       url(r'^checklistitem_add/(?P<id>\w+)/$', ChecklistItemCreate.as_view(), name='checklistitem_add'),
                       url(r'^checklistitem_update/(?P<pk>\w+)/$', ChecklistItemUpdate.as_view(), name='checklistitem_update'),
                       url(r'^checklist_update_link/(?P<pk>\w+)/(?P<type>\w+)/(?P<value>\w+)/$', 'activitydb.views.checklist_update_link', name='checklist_update_link'),
                       url(r'^checklistitem_delete/(?P<pk>\w+)/$', ChecklistItemDelete.as_view(), name='checklistitem_delete'),

                       url(r'^beneficiary_list/(?P<pk>\w+)/$', BeneficiaryList.as_view(), name='beneficiary_list'),
                       url(r'^beneficiary_add/(?P<id>\w+)/$', BeneficiaryCreate.as_view(), name='beneficiary_add'),
                       url(r'^beneficiary_update/(?P<pk>\w+)/$', BeneficiaryUpdate.as_view(), name='beneficiary_update'),
                       url(r'^beneficiary_delete/(?P<pk>\w+)/$', BeneficiaryDelete.as_view(), name='beneficiary_delete'),

                       url(r'^distribution_list/(?P<pk>\w+)/$', DistributionList.as_view(), name='distribution_list'),
                       url(r'^distribution_add/(?P<id>\w+)/$', DistributionCreate.as_view(), name='distribution_add'),
                       url(r'^distribution_update/(?P<pk>\w+)/$', DistributionUpdate.as_view(), name='distribution_update'),
                       url(r'^distribution_delete/(?P<pk>\w+)/$', DistributionDelete.as_view(), name='distribution_delete'),

                       url(r'^budget_list/(?P<pk>\w+)/$', BudgetList.as_view(), name='budget_list'),
                       url(r'^budget_add/(?P<id>\w+)/$', BudgetCreate.as_view(), name='budget_add'),
                       url(r'^budget_update/(?P<pk>\w+)/$', BudgetUpdate.as_view(), name='budget_update'),
                       url(r'^budget_delete/(?P<pk>\w+)/$', BudgetDelete.as_view(), name='budget_delete'),

                       url(r'^report/export/$', 'activitydb.views.report', name='report'),
                       url(r'^report/', 'activitydb.views.report', name='report'),

                       url(r'^province/(?P<province>[-\w]+)/province_json/', 'activitydb.views.province_json', name='province_json'),
                       url(r'^country/(?P<country>[-\w]+)/country_json/', 'activitydb.views.country_json', name='country_json'),
                       url(r'^district/(?P<district>[-\w]+)/district_json/', 'activitydb.views.district_json', name='district_json'),

                       url(r'^custom_dashboard/(?P<pk>[0-9]+)/$', CustomDashboardList.as_view(), name='custom_dashboard_list'),
                       url(r'^custom_dashboard_detail/(?P<pk>[0-9]+)/$', CustomDashboardDetail.as_view(), name='custom_dashboard_detail'),
                       # url(r'^custom_dashboard_preview/(?P<pk>[0-9]+)/$', 'activitydb.views.dashboard_preview_link', name='custom_dashboard_detail'),
                       url(r'^custom_dashboard_add/(?P<id>[0-9]+)/$', CustomDashboardCreate.as_view(), name='custom_dashboard_add'),
                       url(r'^custom_dashboard_update/(?P<pk>[0-9]+)/$', CustomDashboardUpdate.as_view(template_name="customdashboard/admin/customdashboard_form.html"), name='custom_dashboard_update'),
                       url(r'^custom_dashboard_edit/(?P<pk>[0-9]+)/$', CustomDashboardUpdate.as_view(template_name="customdashboard/admin/customdashboard_modal_form.html"), name='custom_dashboard_edit'),
                       url(r'^custom_dashboard_map/(?P<pk>[0-9]+)/(?P<location>[0-9]+)/(?P<type>[-\w]+)/$', CustomDashboardUpdate.as_view(template_name="customdashboard/admin/dashboard_component_map.html"), name='custom_dashboard_map'),
                       url(r'^custom_dashboard_remap/(?P<pk>[0-9]+)/(?P<location>[0-9]+)/(?P<type>[-\w]+)/$', CustomDashboardUpdate.as_view(template_name="customdashboard/admin/dashboard_component_unmap.html"), name='custom_dashboard_unmap'),
                       url(r'^custom_dashboard_delete/(?P<pk>[0-9]+)/$', CustomDashboardDelete.as_view(), name='custom_dashboard_delete'),

                       url(r'^custom_dashboard/theme/$', DashboardThemeList.as_view(), name='dashboard_theme_list'),
                       url(r'^custom_dashboard/theme_add/$',  DashboardThemeCreate.as_view(), name='dashboard_theme_add'),
                       url(r'^custom_dashboard/theme_update/(?P<pk>[0-9]+)/$',  DashboardThemeUpdate.as_view(), name='custom_dashboard/theme_update'),
                       url(r'^custom_dashboard/theme_delete/(?P<pk>[0-9]+)/$', DashboardThemeDelete.as_view(), name='custom_dashboard/theme_delete'),
                      
                       url(r'^custom_dashboard/component/(?P<pk>[0-9]+)/$', DashboardComponentList.as_view(), name='dashboard_component_list'),                       
                       url(r'^custom_dashboard/component_add/(?P<id>[0-9]+)/$', DashboardComponentCreate.as_view(), name='custom_dashboard/component_add'),
                       url(r'^custom_dashboard/component_update/(?P<pk>[0-9]+)/$', DashboardComponentUpdate.as_view(template_name="customdashboard/admin/dashboard_component_update_form.html"), name='custom_dashboard/component_update'),
                       url(r'^custom_dashboard/component_delete/(?P<pk>[0-9]+)/$', DashboardComponentDelete.as_view(), name='custom_dashboard/component_delete'),

                       url(r'^custom_dashboard/data/(?P<pk>[0-9]+)/$', ComponentDataSourceList.as_view(), name='component_data_source_list'),
                       url(r'^custom_dashboard/data_add/$', ComponentDataSourceCreate.as_view(), name='custom_dashboard/data_add'),
                       url(r'^custom_dashboard/data_assign/(?P<pk>[0-9]+)/$', DashboardComponentUpdate.as_view(template_name="customdashboard/admin/component_data_source_assign.html"), name='custom_dashboard/data_assign'),
                       url(r'^custom_dashboard/data_update/(?P<pk>[0-9]+)/$', ComponentDataSourceUpdate.as_view(), name='custom_dashboard/data_update'),
                       url(r'^custom_dashboard/data_delete/(?P<pk>[0-9]+)/$', ComponentDataSourceDelete.as_view(), name='custom_dashboard/data_delete'),
                       
                       #ajax calls
                       url(r'^service/(?P<service>[-\w]+)/service_json/', 'indicators.views.service_json', name='service_json'),

                       ]
