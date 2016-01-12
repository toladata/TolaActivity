from feed import views
from tola import views
from feed.views import UserViewSet, ProgramViewSet, SectorViewSet, ProjectTypeViewSet, OfficeViewSet, SiteProfileViewSet, AgreementViewSet, \
    CompleteViewSet, CountryViewSet, ProjectTypeOtherViewSet, IndicatorViewSet, ReportingFrequencyViewSet, TolaUserViewSet, IndicatorTypeViewSet, ObjectiveViewSet, DisaggregationTypeViewSet, LevelViewSet
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, serializers, viewsets
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import login, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#REST FRAMEWORK
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'programs', ProgramViewSet)
router.register(r'sector', SectorViewSet)
router.register(r'projecttype', ProjectTypeViewSet)
router.register(r'office', OfficeViewSet)
router.register(r'siteprofile', SiteProfileViewSet)
router.register(r'country', CountryViewSet)
router.register(r'agreements', AgreementViewSet)
router.register(r'completes', CompleteViewSet)
router.register(r'projecttypeother', ProjectTypeOtherViewSet)
router.register(r'indicator', IndicatorViewSet)
router.register(r'reportingfrequency', ReportingFrequencyViewSet)
router.register(r'tolauser', TolaUserViewSet)
router.register(r'indicatortype', IndicatorTypeViewSet)
router.register(r'objective', ObjectiveViewSet)
router.register(r'disaggregationtype', DisaggregationTypeViewSet)
router.register(r'level', LevelViewSet)




urlpatterns = patterns('',
                        #rest framework
                        url(r'^api/', include(router.urls)),
                        url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

                        #index
                        url(r'^$', 'tola.views.index', name='index'),
                        #enable the admin:
                        url(r'^admin/', include(admin.site.urls)),
                        url(r'^(?P<selected_countries>\w+)/$', 'tola.views.index', name='index'),

                        #index
                        url(r'^dashboard/(?P<id>\w+)/(?P<sector>\w+)/$', 'tola.views.index', name='index'),

                        #base template for layout
                        url(r'^$', TemplateView.as_view(template_name='base.html')),

                        #ipt app specific urls
                        #url(r'^indicators/', include('indicators.urls')),

                        #enable admin documentation:
                        url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                        #home
                        url(r'^contact', 'tola.views.contact', name='contact'),
                        url(r'^faq', 'tola.views.faq', name='faq'),
                        url(r'^documentation', 'tola.views.documentation', name='documentation'),

                        #app include of activitydb urls
                        url(r'^activitydb/', include('activitydb.urls')),

                        #app include of activitydb urls
                        url(r'^indicators/', include('indicators.urls')),

                        #app include of customdashboard urls
                        url(r'^customdashboard/', include('customdashboard.urls')),

                        #local login
                        url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
                        url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
                        url(r'^accounts/logout/$', 'tola.views.logout_view', name='logout'),

                        #accounts
                        url(r'^accounts/profile/$', 'tola.views.profile', name='profile'),
                        url(r'^accounts/register/$', 'tola.views.register', name='register'),

                        #Auth backend URL's
                        url('', include('django.contrib.auth.urls', namespace='auth')),
                        url('', include('social.apps.django_app.urls', namespace='social')),



)  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

