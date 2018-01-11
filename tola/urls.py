from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import routers

from formlibrary.views import BinaryFieldViewSet, binary_test
from tola import views as tola_views
from tola.views import *
from feed.views import *
from search.views import *

admin.autodiscover()
admin.site.site_header = 'TolaActivity administration'


# REST FRAMEWORK
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'tolauser', TolaUserViewSet)
router.register(r'tolauserfilter', TolaUserFilterViewSet)
router.register(r'organization', OrganizationViewSet)
router.register(r'country', CountryViewSet)
router.register(r'award', AwardViewSet)
router.register(r'workflowlevel1', WorkflowLevel1ViewSet)
router.register(r'workflowlevel2', WorkflowLevel2ViewSet)
router.register(r'workflowlevel2sort', WorkflowLevel2SortViewSet)
router.register(r'workflowmodules', WorkflowModulesViewSet)
router.register(r'workflowteam', WorkflowTeamViewSet)
router.register(r'workflowlevel1sector', WorkflowLevel1SectorViewSet)
router.register(r'approvaltype', ApprovalTypeViewSet)
router.register(r'approvalworkflow', ApprovalWorkflowViewSet)
router.register(r'milestone', MilestoneViewSet)
router.register(r'checklist', ChecklistViewSet)
router.register(r'sector', SectorViewSet)
router.register(r'projecttype', ProjectTypeViewSet)
router.register(r'office', OfficeViewSet)
router.register(r'budget', BudgetViewSet)
router.register(r'fundcode', FundCodeViewSet)
router.register(r'siteprofile', SiteProfileViewSet)
router.register(r'adminboundaryone', ProvinceViewSet)
router.register(r'adminboundarytwo', DistrictViewSet)
router.register(r'adminboundarythree', AdminLevelThreeViewSet)
router.register(r'adminboundaryfour', VillageViewSet)
router.register(r'frequency', FrequencyViewSet)
router.register(r'indicatortype', IndicatorTypeViewSet)
router.register(r'indicator', IndicatorViewSet)
router.register(r'objective', ObjectiveViewSet)
router.register(r'strategicobjective', StrategicObjectiveViewSet)
router.register(r'level', LevelViewSet)
router.register(r'externalservice', ExternalServiceViewSet)
router.register(r'externalservicerecord', ExternalServiceRecordViewSet)
router.register(r'stakeholder', StakeholderViewSet)
router.register(r'stakeholdertype', StakeholderTypeViewSet)
router.register(r'profiletype', ProfileTypeViewSet)
router.register(r'contact', ContactViewSet)
router.register(r'documentation', DocumentationViewSet)
router.register(r'collecteddata', CollectedDataViewSet)
router.register(r'periodictarget', PeriodicTargetViewSet)
router.register(r'tolatable', TolaTableViewSet, base_name='tolatable')
router.register(r'disaggregationtype', DisaggregationTypeViewSet)
router.register(r'disaggregationlabel', DisaggregationLabelViewSet)
router.register(r'disaggregationvalue', DisaggregationValueViewSet)
router.register(r'checklist', ChecklistViewSet)
router.register(r'organization', OrganizationViewSet)
router.register(r'currency', CurrencyViewSet)
router.register(r'beneficiary', BeneficiaryViewSet)
router.register(r'riskregister', RiskRegisterViewSet)
router.register(r'issueregister', IssueRegisterViewSet)
router.register(r'fieldtype', FieldTypeViewSet)
router.register(r'customformfield', CustomFormFieldViewSet)
router.register(r'customform', CustomFormViewSet)
router.register(r'codedfield', CodedFieldViewSet)
router.register(r'codedfieldvalues', CodedFieldValuesViewSet)
router.register(r'landtype', LandTypeViewSet)
router.register(r'internationalization', InternationalizationViewSet)
router.register(r'dashboard', DashboardViewSet)
#router.register(r'public_dashboard', PublicDashboardViewSet)
#router.register(r'org_dashboard', PublicOrgDashboardViewSet)
router.register(r'widget', WidgetViewSet)
router.register(r'portfolio', PortfolioViewSet)
router.register(r'sectorrelated', SectorRelatedViewSet)
router.register(r'pindicators', ProgramIndicatorReadOnlyViewSet, base_name='pindicators')

# router.register(r'search', SearchView, base_name='search')

router.register(r'binary', BinaryFieldViewSet, base_name='binary')
router.register(r'pindicators', ProgramIndicatorReadOnlyViewSet, base_name='pindicators')
urlpatterns = [ # rest framework
                url(r'^check', tola_views.check_view),
                url(r'^dev_loader', tola_views.dev_view),
                url(r'^api/', include(router.urls)),
                url(r'^binarytest/(?P<id>\w+)', binary_test),
                url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

                # index
                url(r'^$', tola_views.IndexView.as_view(), name='index'),

                # enable the admin:
                url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                url(r'^admin/', include(admin.site.urls)),

                # enable admin documentation:
                url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                # app include of workflow urls
                url(r'^workflow/', include('workflow.urls')),

                # app include of indicator urls
                url(r'^indicators/', include('indicators.urls')),

                # app include of customdashboard urls
                url(r'^customdashboard/', include('customdashboard.urls')),

                # app include of reports urls
                url(r'^reports/', include('reports.urls')),

                # app include of workflow urls
                url(r'^formlibrary/', include('formlibrary.urls')),

                # local login
                url(r'^accounts/login/$', auth_views.login, name='login'),
                url(r'^accounts/logout/$', tola_views.logout_view, name='logout'),

                # accounts
                url(r'^accounts/profile/$', tola_views.profile, name='profile'),
                url(r'^accounts/register/$', tola_views.RegisterView.as_view(), name='register'),

                # bookmarks
                url(r'^bookmark_list', BookmarkList.as_view(), name='bookmark_list'),
                url(r'^bookmark_add', BookmarkCreate.as_view(), name='bookmark_add'),
                url(r'^bookmark_update/(?P<pk>\w+)/$', BookmarkUpdate.as_view(), name='bookmark_update'),
                url(r'^bookmark_delete/(?P<pk>\w+)/$', BookmarkDelete.as_view(), name='bookmark_delete'),

                # Search app URL's
                url(r'^search/', include('search.urls')),

                # Auth backend URL's
                url('', include('django.contrib.auth.urls', namespace='auth')),
                url('', include('social_django.urls', namespace='social')),

                url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
                url(r'^oauthuser', OAuth_User_Endpoint.as_view()),
                url(r'^tolatrack/silo', TolaTrackSiloProxy.as_view()),
                url(r'^tolatrackdata/silo/(?P<silo_id>\w+)/$', TolaTrackSiloDataProxy.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    try:
        import debug_toolbar
    except ImportError:
        pass
    else:
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
