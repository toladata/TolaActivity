from .views import ProgramDash, ProjectAgreementCreate, ProjectAgreementList, ProjectAgreementUpdate, ProjectAgreementDetail, ProjectAgreementDelete, ProjectAgreementImport, ProjectCompleteCreate, ProjectCompleteUpdate,\
    ProjectCompleteList, ProjectCompleteDelete, ProjectCompleteImport, CommunityList, CommunityCreate, CommunityUpdate, CommunityDelete,\
    DocumentationList, DocumentationCreate, DocumentationUpdate, DocumentationDelete,ProjectDash, MonitorList,MonitorCreate, MonitorDelete, MonitorUpdate,\
    BenchmarkCreate, BenchmarkDelete, BenchmarkUpdate, TrainingUpdate, TrainingCreate, TrainingDelete, TrainingList, BeneficiaryList, BeneficiaryCreate, BeneficiaryUpdate,\
    BeneficiaryDelete, ProjectCompleteDetail, CommunityReport, ChecklistCreate, ChecklistDelete, ChecklistUpdate, BudgetList, QuantitativeOutputsList, QuantitativeOutputsCreate, QuantitativeOutputsUpdate, QuantitativeOutputsDelete,\
    ChecklistCreate, ChecklistDelete, ChecklistUpdate, ChecklistList, BudgetCreate, BudgetUpdate, BudgetDelete

from django.conf.urls import *

# place app url patterns here

urlpatterns = patterns('',
                       url(r'^report_builder/', include('report_builder.urls')),
                       ###activitydb
                       url(r'^dashboard/(?P<pk>\w+)/$', ProgramDash.as_view(), name='dashboard'),
                       url(r'^dashboard/project/(?P<pk>\w+)/$', ProjectDash.as_view(), name='project_dashboard'),

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

                       url(r'^community_list/(?P<program_id>\w+)/(?P<activity_id>\w+)/$', CommunityList.as_view(), name='community_list'),
                       url(r'^community_report/(?P<pk>\w+)/$', CommunityReport.as_view(), name='community_report'),
                       url(r'^community_add', CommunityCreate.as_view(), name='community_add'),
                       url(r'^community_update/(?P<pk>\w+)/$', CommunityUpdate.as_view(), name='community_update'),
                       url(r'^community_delete/(?P<pk>\w+)/$', CommunityDelete.as_view(), name='community_delete'),

                       url(r'^documentation_list/(?P<pk>\w+)/$', DocumentationList.as_view(), name='documentation_list'),
                       url(r'^documentation_add', DocumentationCreate.as_view(), name='documentation_add'),
                       url(r'^documentation_update/(?P<pk>\w+)/$', DocumentationUpdate.as_view(), name='documentation_update'),
                       url(r'^documentation_delete/(?P<pk>\w+)/$', DocumentationDelete.as_view(), name='documentation_delete'),

                       url(r'^monitor_list/(?P<pk>\w+)/$', MonitorList.as_view(), name='monitor_list'),
                       url(r'^monitor_add/(?P<id>\w+)/$', MonitorCreate.as_view(), name='monitor_add'),
                       url(r'^monitor_update/(?P<pk>\w+)/$', MonitorUpdate.as_view(), name='monitor_update'),
                       url(r'^monitor_delete/(?P<pk>\w+)/$', MonitorDelete.as_view(), name='monitor_delete'),

                       url(r'^quantitative_list/(?P<pk>\w+)/$', QuantitativeOutputsList.as_view(), name='quantitative_list'),
                       url(r'^quantitative_add/(?P<id>\w+)/$', QuantitativeOutputsCreate.as_view(), name='quantitative_add'),
                       url(r'^quantitative_update/(?P<pk>\w+)/$', QuantitativeOutputsUpdate.as_view(), name='quantitative_update'),
                       url(r'^quantitative_delete/(?P<pk>\w+)/$', QuantitativeOutputsDelete.as_view(), name='quantitative_delete'),


                       url(r'^benchmark_add/(?P<id>\w+)/$', BenchmarkCreate.as_view(), name='benchmark_add'),
                       url(r'^benchmark_update/(?P<pk>\w+)/$', BenchmarkUpdate.as_view(), name='benchmark_update'),
                       url(r'^benchmark_delete/(?P<pk>\w+)/$', BenchmarkDelete.as_view(), name='benchmark_delete'),

                       url(r'^training_list/(?P<pk>\w+)/$', TrainingList.as_view(), name='training_list'),
                       url(r'^training_add/(?P<id>\w+)/$', TrainingCreate.as_view(), name='training_add'),
                       url(r'^training_update/(?P<pk>\w+)/$', TrainingUpdate.as_view(), name='training_update'),
                       url(r'^training_delete/(?P<pk>\w+)/$', TrainingDelete.as_view(), name='training_delete'),

                       url(r'^checklist_list/(?P<pk>\w+)/$', ChecklistList.as_view(), name='checklist_list'),
                       url(r'^checklist_add/(?P<id>\w+)/$', ChecklistCreate.as_view(), name='checklist_add'),
                       url(r'^checklist_update/(?P<pk>\w+)/$', ChecklistUpdate.as_view(), name='checklist_update'),
                       url(r'^checklist_delete/(?P<pk>\w+)/$', ChecklistDelete.as_view(), name='checklistdelete'),

                       url(r'^beneficiary_list/(?P<pk>\w+)/$', BeneficiaryList.as_view(), name='beneficiary_list'),
                       url(r'^beneficiary_add/(?P<id>\w+)/$', BeneficiaryCreate.as_view(), name='beneficiary_add'),
                       url(r'^beneficiary_update/(?P<pk>\w+)/$', BeneficiaryUpdate.as_view(), name='beneficiary_update'),
                       url(r'^beneficiary_delete/(?P<pk>\w+)/$', BeneficiaryDelete.as_view(), name='beneficiary_delete'),

                       url(r'^budget_list/(?P<pk>\w+)/$', BudgetList.as_view(), name='budget_list'),
                       url(r'^budget_add/(?P<id>\w+)/$', BudgetCreate.as_view(), name='budget_add'),
                       url(r'^budget_update/(?P<pk>\w+)/$', BudgetUpdate.as_view(), name='budget_update'),
                       url(r'^budget_delete/(?P<pk>\w+)/$', BudgetDelete.as_view(), name='budget_delete'),

                       url(r'^report/', 'activitydb.views.report', name='report'),

                       url(r'^province/(?P<province>[-\w]+)/province_json/', 'activitydb.views.province_json', name='province_json'),

                       url(r'^count/$', 'activitydb.views.ProgramDashboardCounts', name='ProgramDashboardCounts'),


                       )
