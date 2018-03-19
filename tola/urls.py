import os

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework import routers

from formlibrary.views import BinaryFieldViewSet, binary_test
from tola import views as tola_views
from feed import views as feed_views
from tola import DEMO_BRANCH

admin.autodiscover()
admin.site.site_header = 'TolaActivity administration'


# REST FRAMEWORK
router = routers.DefaultRouter()
router.register(r'users', feed_views.UserViewSet)
router.register(r'groups', feed_views.GroupViewSet)
router.register(r'tolauser', feed_views.TolaUserViewSet)
router.register(r'tolauserfilter', feed_views.TolaUserFilterViewSet)
router.register(r'organization', feed_views.OrganizationViewSet)
router.register(r'country', feed_views.CountryViewSet)
router.register(r'award', feed_views.AwardViewSet)
router.register(r'workflowlevel1', feed_views.WorkflowLevel1ViewSet)
router.register(r'workflowlevel2', feed_views.WorkflowLevel2ViewSet)
router.register(r'workflowlevel2sort', feed_views.WorkflowLevel2SortViewSet)
router.register(r'workflowmodules', feed_views.WorkflowModulesViewSet)
router.register(r'workflowteam', feed_views.WorkflowTeamViewSet)
router.register(r'workflowlevel1sector', feed_views.WorkflowLevel1SectorViewSet)
router.register(r'approvaltype', feed_views.ApprovalTypeViewSet)
router.register(r'approvalworkflow', feed_views.ApprovalWorkflowViewSet)
router.register(r'milestone', feed_views.MilestoneViewSet)
router.register(r'checklist', feed_views.ChecklistViewSet)
router.register(r'sector', feed_views.SectorViewSet)
router.register(r'projecttype', feed_views.ProjectTypeViewSet)
router.register(r'office', feed_views.OfficeViewSet)
router.register(r'budget', feed_views.BudgetViewSet)
router.register(r'fundcode', feed_views.FundCodeViewSet)
router.register(r'siteprofile', feed_views.SiteProfileViewSet)
router.register(r'adminboundaryone', feed_views.ProvinceViewSet)
router.register(r'adminboundarytwo', feed_views.DistrictViewSet)
router.register(r'adminboundarythree', feed_views.AdminLevelThreeViewSet)
router.register(r'adminboundaryfour', feed_views.VillageViewSet)
router.register(r'frequency', feed_views.FrequencyViewSet)
router.register(r'indicatortype', feed_views.IndicatorTypeViewSet)
router.register(r'indicator', feed_views.IndicatorViewSet)
router.register(r'objective', feed_views.ObjectiveViewSet)
router.register(r'strategicobjective', feed_views.StrategicObjectiveViewSet)
router.register(r'level', feed_views.LevelViewSet)
router.register(r'externalservice', feed_views.ExternalServiceViewSet)
router.register(r'externalservicerecord', feed_views.ExternalServiceRecordViewSet)
router.register(r'stakeholder', feed_views.StakeholderViewSet)
router.register(r'stakeholdertype', feed_views.StakeholderTypeViewSet)
router.register(r'profiletype', feed_views.ProfileTypeViewSet)
router.register(r'contact', feed_views.ContactViewSet)
router.register(r'documentation', feed_views.DocumentationViewSet)
router.register(r'collecteddata', feed_views.CollectedDataViewSet)
router.register(r'periodictarget', feed_views.PeriodicTargetViewSet)
router.register(r'tolatable', feed_views.TolaTableViewSet, base_name='tolatable')
router.register(r'disaggregationtype', feed_views.DisaggregationTypeViewSet)
router.register(r'disaggregationlabel', feed_views.DisaggregationLabelViewSet)
router.register(r'disaggregationvalue', feed_views.DisaggregationValueViewSet)
router.register(r'checklist', feed_views.ChecklistViewSet)
router.register(r'organization', feed_views.OrganizationViewSet)
router.register(r'currency', feed_views.CurrencyViewSet)
router.register(r'beneficiary', feed_views.BeneficiaryViewSet)
router.register(r'riskregister', feed_views.RiskRegisterViewSet)
router.register(r'issueregister', feed_views.IssueRegisterViewSet)
router.register(r'fieldtype', feed_views.FieldTypeViewSet)
router.register(r'customformfield', feed_views.CustomFormFieldViewSet)
router.register(r'customform', feed_views.CustomFormViewSet)
router.register(r'codedfield', feed_views.CodedFieldViewSet)
router.register(r'codedfieldvalues', feed_views.CodedFieldValuesViewSet)
router.register(r'landtype', feed_views.LandTypeViewSet)
router.register(r'internationalization', feed_views.InternationalizationViewSet)
router.register(r'dashboard', feed_views.DashboardViewSet)
router.register(r'widget', feed_views.WidgetViewSet)
router.register(r'portfolio', feed_views.PortfolioViewSet)
router.register(r'sectorrelated', feed_views.SectorRelatedViewSet)
router.register(r'pindicators', feed_views.ProgramIndicatorReadOnlyViewSet, base_name='pindicators')
# router.register(r'search', search_views.SearchView, base_name='search')
router.register(r'binary', BinaryFieldViewSet, base_name='binary')

urlpatterns = [
    # Rest framework
    url(r'^check', tola_views.check_view),
    url(r'^api/', include(router.urls)),
    url(r'^binarytest/(?P<id>\w+)', binary_test),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Admin:
    url(r'^admin/', include(admin.site.urls)),

    # Index / Homepage
    url(r'^$', tola_views.IndexView.as_view(), name='index'),

    # App include of workflow urls
    url(r'^workflow/', include('workflow.urls')),

    # App include of indicator urls
    url(r'^indicators/', include('indicators.urls')),

    # App include of customdashboard urls
    url(r'^customdashboard/', include('customdashboard.urls')),

    # App include of reports urls
    url(r'^reports/', include('reports.urls')),

    # App include of workflow urls
    url(r'^formlibrary/', include('formlibrary.urls')),

    # Local login
    url(r'^accounts/login/$', auth_views.LoginView.as_view(
        extra_context={
            'chargebee_signup_org_url': settings.CHARGEBEE_SIGNUP_ORG_URL,
            'is_demo_branch': os.getenv('APP_BRANCH') == DEMO_BRANCH
        }),
        name='login'),
    url(r'^accounts/logout/$', tola_views.logout_view, name='logout'),

    # Accounts
    url(r'^accounts/profile/$', tola_views.profile, name='profile'),
    url(r'^accounts/register/$', tola_views.RegisterView.as_view(), name='register'),

    # Bookmarks
    url(r'^bookmark_list', tola_views.BookmarkList.as_view(), name='bookmark_list'),
    url(r'^bookmark_add', tola_views.BookmarkCreate.as_view(), name='bookmark_add'),
    url(r'^bookmark_update/(?P<pk>\w+)/$', tola_views.BookmarkUpdate.as_view(), name='bookmark_update'),
    url(r'^bookmark_delete/(?P<pk>\w+)/$', tola_views.BookmarkDelete.as_view(), name='bookmark_delete'),

    # Search app URL's
    url(r'^search/', include('search.urls')),

    # Auth backend URL's
    url('', include('django.contrib.auth.urls', namespace='auth')),
    url('', include('social_django.urls', namespace='social')),

    url(r'^oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^oauthuser', tola_views.OAuthUserEndpoint.as_view()),
    url(r'^tolatrack/silo', tola_views.TolaTrackSiloProxy.as_view()),
    url(r'^tolatrackdata/silo/(?P<silo_id>\w+)/$', tola_views.TolaTrackSiloDataProxy.as_view()),
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
