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
from tola import DEMO_BRANCH

admin.autodiscover()
admin.site.site_header = 'TolaActivity administration'


# REST FRAMEWORK
router = routers.DefaultRouter()
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
