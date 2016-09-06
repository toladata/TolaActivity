from feed import views
from tola import views
from feed.views import *
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, serializers, viewsets
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout
from rest_framework.authtoken import views as auth_views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
admin.site.site_header = 'Tola Activity administration'

#REST FRAMEWORK
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'programs', ProgramViewSet)
router.register(r'sector', SectorViewSet)
router.register(r'projecttype', ProjectTypeViewSet)
router.register(r'office', OfficeViewSet)
router.register(r'siteprofile', SiteProfileViewSet)
router.register(r'country', CountryViewSet)
router.register(r'initiations', AgreementViewSet)
router.register(r'tracking', CompleteViewSet)
router.register(r'indicator', IndicatorViewSet)
router.register(r'reportingfrequency', ReportingFrequencyViewSet)
router.register(r'tolauser', TolaUserViewSet)
router.register(r'indicatortype', IndicatorTypeViewSet)
router.register(r'objective', ObjectiveViewSet)
router.register(r'disaggregationtype', DisaggregationTypeViewSet)
router.register(r'level', LevelViewSet)
router.register(r'customdashboard', CustomDashboardViewSet)
router.register(r'externalservice', ExternalServiceViewSet)
router.register(r'externalservicerecord', ExternalServiceRecordViewSet)
router.register(r'strategicobjective', StrategicObjectiveViewSet)
router.register(r'stakeholder', StakeholderViewSet)
router.register(r'stakeholdertype', StakeholderTypeViewSet)
router.register(r'capacity', CapacityViewSet)
router.register(r'evaluate', EvaluateViewSet)
router.register(r'profiletype', ProfileTypeViewSet)
router.register(r'province', ProvinceViewSet)
router.register(r'district', DistrictViewSet)
router.register(r'adminlevelthree', AdminLevelThreeViewSet)
router.register(r'village', VillageViewSet)
router.register(r'contact', ContactViewSet)
router.register(r'documentation', DocumentationViewSet)
router.register(r'collecteddata', CollectedDataViewSet)
router.register(r'tolatable', TolaTableViewSet)
router.register(r'disaggregationvalue', DisaggregationValueViewSet)
router.register(r'projectagreements', ProjectAgreementViewSet)
router.register(r'loggedusers', LoggedUserSerializerViewSet)


urlpatterns = [ # rest framework
                url(r'^api/', include(router.urls)),
                url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                url(r'^api-token-auth/', auth_views.obtain_auth_token),

                # index
                url(r'^$', views.index, name='index'),
                # enable the admin:
                url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
                url(r'^admin/', include(admin.site.urls)),
                url(r'^(?P<selected_countries>\w+)/$', views.index, name='index'),

                # index
                url(r'^dashboard/(?P<id>\w+)/(?P<sector>\w+)/$', 'tola.views.index', name='index'),

                # base template for layout
                url(r'^$', TemplateView.as_view(template_name='base.html')),

                # enable admin documentation:
                url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                # home
                url(r'^contact', views.contact, name='contact'),
                url(r'^faq', views.faq, name='faq'),
                url(r'^documentation', views.documentation, name='documentation'),

                # app include of activitydb urls
                url(r'^activitydb/', include('activitydb.urls')),

                # app include of indicator urls
                url(r'^indicators/', include('indicators.urls')),

                # app include of customdashboard urls
                url(r'^customdashboard/', include('customdashboard.urls')),

                # app include of reports urls
                url(r'^reports/', include('reports.urls')),

                # app include of tables urls
                url(r'^tables/', include('tables.urls')),

                # local login
                url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
                url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
                url(r'^accounts/logout/$', views.logout_view, name='logout'),

                # accounts
                url(r'^accounts/profile/$', views.profile, name='profile'),
                url(r'^accounts/register/$', views.register, name='register'),

                # Auth backend URL's
                url('', include('django.contrib.auth.urls', namespace='auth')),
                url('', include('social.apps.django_app.urls', namespace='social')),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
