from tola import views
from tola.views import *
from feed.views import *
from search.views import *
from django.conf.urls import include, url
from django.views.generic import TemplateView
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.authtoken import views as auth_views
from django.contrib.auth import views as authviews
from django.contrib.auth import forms as authforms

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
admin.site.site_header = 'Tola Activity administration'

#REST FRAMEWORK
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'tolauser', TolaUserViewSet)
router.register(r'tolauserfilter', TolaUserFilterViewSet)
router.register(r'organization', OrganizationViewSet)
router.register(r'country', CountryViewSet)
router.register(r'workflowlevel1', WorkflowLevel1ViewSet)
router.register(r'workflowlevel2', WorkflowLevel2ViewSet)
router.register(r'workflowlevel2sort', WorkflowLevel2SortViewSet)
router.register(r'workflowmodules', WorkflowModulesViewSet)
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
router.register(r'reportingfrequency', ReportingFrequencyViewSet)
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
router.register(r'tolatable', TolaTableViewSet)
router.register(r'disaggregationtype', DisaggregationTypeViewSet)
router.register(r'dissagregationlabel', DisaggregationLabelViewSet)
router.register(r'disaggregationvalue', DisaggregationValueViewSet)
router.register(r'checklist', ChecklistViewSet)
router.register(r'organization', OrganizationViewSet)
router.register(r'currency', CurrencyViewSet)
router.register(r'approvaltype', ApprovalTypeViewSet)
router.register(r'approvalworkflow', ApprovalWorkflowViewSet)
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
router.register(r'pindicators', ProgramIndicatorReadOnlyViewSet, base_name='pindicators')
router.register(r'award', AwardViewSet, base_name='award')
#router.register(r'search', SearchView, base_name='search')

from formlibrary.views import BinaryFieldViewSet, binary_test
router.register(r'binary', BinaryFieldViewSet, base_name='binary')


urlpatterns = [ # rest framework
                url(r'^check', views.check_view),
                url(r'^api/', include(router.urls)),
                url(r'^binarytest/(?P<id>\w+)', binary_test),
                url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                url(r'^api-token-auth/', auth_views.obtain_auth_token),

                # index
                url(r'^$', views.index, name='index'),
                # enable the admin:
                url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                url(r'^admin/', include(admin.site.urls)),
                url(r'^(?P<selected_countries>\w+)/$', views.index, name='index'),

                # index
                url(r'^dashboard/(?P<id>\w+)/(?P<sector>\w+)/$', views.index, name='index'),

                # base template for layout
                url(r'^$', TemplateView.as_view(template_name='base.html')),

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
                url(r'^login/$', authviews.login, name='login'),
                url(r'^accounts/login/$', authviews.login, name='login'),
                #url(r'^accounts/login/$', authviews.login, {'template_name': 'login.html'}, name="login") ,

                url(r'^accounts/logout/$', authviews.LogoutView.as_view(), name='logout'),

                # accounts
                url(r'^accounts/profile/$', views.profile, name='profile'),
                url(r'^accounts/register/$', views.register, name='register'),

                #bookmarks
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

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
