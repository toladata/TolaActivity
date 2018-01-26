from importlib import import_module
import json
import logging
import os
import sys
from urlparse import urljoin

from chargebee import InvalidRequestError, Subscription

from django.contrib import auth
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.sites.models import Site
from django.core.urlresolvers import clear_url_caches
from django.test import Client, RequestFactory, TestCase, override_settings
from django.conf import settings
from django.urls import reverse
from mock import Mock, patch

import factories
from tola import views, DEMO_BRANCH
from workflow.models import (Organization, TolaUser, TolaSites, ROLE_VIEW_ONLY,
                             TITLE_CHOICES)


# TODO Extend View tests


class IndexViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.tola_user = factories.TolaUser()

    def test_dispatch_unauthenticated(self):
        request = self.factory.get('', follow=True)
        request.user = AnonymousUser()
        response = views.IndexView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    @override_settings(TOLA_ACTIVITY_URL='https://tolaactivity.com')
    @override_settings(TOLA_TRACK_URL='https://tolatrack.com/')
    def test_dispatch_authenticated_with_urls_set(self):
        request = self.factory.get('')
        request.user = self.tola_user.user
        response = views.IndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['tolaactivity_url'],
                         'https://tolaactivity.com')
        self.assertEqual(response.context_data['tolatrack_url'],
                         'https://tolatrack.com/')
        template_content = response.render().content
        self.assertIn('https://tolaactivity.com', template_content)
        self.assertIn('https://tolatrack.com/', template_content)

    @override_settings(TOLA_ACTIVITY_URL='')
    @override_settings(TOLA_TRACK_URL='')
    def test_dispatch_authenticated_with_urls_not_set(self):
        site = Site.objects.create(domain='api.toladata.com', name='API')
        TolaSites.objects.create(
            name='TolaData',
            front_end_url='https://tolaactivity.com',
            tola_tables_url='https://tolatrack.com',
            site=site)

        request = self.factory.get('')
        request.user = self.tola_user.user
        response = views.IndexView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['tolaactivity_url'],
                         'https://tolaactivity.com')
        self.assertEqual(response.context_data['tolatrack_url'],
                         'https://tolatrack.com')
        template_content = response.render().content
        self.assertIn('https://tolaactivity.com', template_content)
        self.assertIn('https://tolatrack.com', template_content)


class LoginViewTest(TestCase):
    def _reload_urlconf(self):
        clear_url_caches()
        if settings.ROOT_URLCONF in sys.modules:
            reload(sys.modules[settings.ROOT_URLCONF])
        return import_module(settings.ROOT_URLCONF)

    @override_settings(CHARGEBEE_SIGNUP_ORG_URL='')
    def test_org_signup_link(self):
        # As the url_patterns are cached when python load the module, also the
        # settings are cached there. As we want to override a setting, we need
        # to reload also the urls in order to catch the new value.
        self._reload_urlconf()
        response = self.client.get(reverse('login'), follow=True)
        template_content = response.content
        self.assertIn(
            ('<a href="#" data-toggle="modal" data-target="#exampleModal">'
             'Register Your Organization with TolaData</a>'),
            template_content)

    @override_settings(CHARGEBEE_SIGNUP_ORG_URL='https://chargebee.com/123')
    def test_org_signup_link_chargebee(self):
        # As the url_patterns are cached when python load the module, also the
        # settings are cached there. As we want to override a setting, we need
        # to reload also the urls in order to catch the new value.
        self._reload_urlconf()
        response = self.client.get(reverse('login'), follow=True)
        template_content = response.content
        self.assertIn(
            ('<a href="https://chargebee.com/123">'
             'Register Your Organization with TolaData</a>'),
            template_content)


class RegisterViewGetTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_with_disclaimer_in_tolasite(self):
        site = Site.objects.create(domain='api.toladata.com', name='API')
        TolaSites.objects.create(
            name='TolaData',
            privacy_disclaimer='Nice disclaimer',
            site=site)

        request = self.factory.get('')
        response = views.RegisterView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        template_content = response.content
        self.assertIn('Nice disclaimer', template_content)

    def test_get_with_disclaimer_in_template(self):
        request = self.factory.get('')
        response = views.RegisterView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        template_content = response.content
        self.assertIn('Humanitec - Privacy Policy', template_content)
        self.assertIn('Privacy disclaimer accepted', template_content)

    def test_get_with_chargebee_active_sub_in_template(self):
        class ExternalResponse:
            def __init__(self, values):
                self.subscription = Subscription(values)
                self.subscription.status = 'active'

        external_response = ExternalResponse(None)
        Subscription.retrieve = Mock(return_value=external_response)
        query_params = '?cus_fname={}&cus_lname={}&cus_email={}&cus_company={}'\
                       '&sub_id={}'.format('John', 'Lennon',
                                           'johnlennon@test.com', 'The Beatles',
                                           '1234567890')
        request = self.factory.get('/accounts/register/{}'.format(query_params))
        response = views.RegisterView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        template_content = response.content

        self.assertIn(
            ('<input type="text" name="first_name" value="John" '
             'id="id_first_name" class="textinput textInput '
             'form-control" maxlength="30" />'),
            template_content)
        self.assertIn(
            ('<input type="text" name="last_name" value="Lennon" '
             'id="id_last_name" class="textinput textInput '
             'form-control" maxlength="30" />'),
            template_content)
        self.assertIn(
            ('<input type="email" name="email" value="johnlennon@test.com" '
             'id="id_email" class="emailinput form-control" '
             'maxlength="254" />'),
            template_content)
        self.assertIn(
            ('<input type="text" name="org" value="The Beatles" required '
             'class="textinput textInput form-control" id="id_org" />'),
            template_content)
        org = Organization.objects.get(name='The Beatles')
        self.assertEqual(org.chargebee_subscription_id, '1234567890')

    def test_get_with_chargebee_cancel_sub_in_template(self):
        class ExternalResponse:
            def __init__(self, values):
                self.subscription = Subscription(values)
                self.subscription.status = 'cancelled'

        external_response = ExternalResponse(None)
        Subscription.retrieve = Mock(return_value=external_response)
        query_params = '?cus_fname={}&cus_lname={}&cus_email={}&cus_company={}'\
                       '&sub_id={}'.format('John', 'Lennon',
                                           'johnlennon@test.com', 'The Beatles',
                                           '1234567890')
        request = self.factory.get('/accounts/register/{}'.format(query_params))
        response = views.RegisterView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertRaises(
            Organization.DoesNotExist,
            Organization.objects.get, name='The Beatles')

    def test_get_with_chargebee_demo(self):
        class ExternalResponse:
            def __init__(self, values):
                self.subscription = Subscription(values)
                self.subscription.status = 'active'

        os.environ['APP_BRANCH'] = DEMO_BRANCH
        query_params = '?cus_fname={}&cus_lname={}&cus_email={}&cus_company={}'\
                       '&sub_id={}'.format('John', 'Lennon',
                                           'johnlennon@test.com', 'The Beatles',
                                           '1234567890')
        request = self.factory.get('/accounts/register/{}'.format(query_params))
        response = views.RegisterView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertRaises(
            Organization.DoesNotExist,
            Organization.objects.get, name='The Beatles')
        os.environ['APP_BRANCH'] = ''

    def test_get_with_chargebee_without_sub_in_template(self):
        json_obj = {
            'message': "Sorry, we couldn't find that resource",
            'error_code': 500
        }
        external_response = InvalidRequestError(500, json_obj)
        Subscription.retrieve = Mock(return_value=external_response)
        query_params = '?cus_fname={}&cus_lname={}&cus_email={}&cus_company=' \
                       '{}'.format('John', 'Lennon', 'johnlennon@test.com',
                                   'The Beatles')
        request = self.factory.get('/accounts/register/{}'.format(query_params))
        response = views.RegisterView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertRaises(
            Organization.DoesNotExist,
            Organization.objects.get, name='The Beatles')


class RegisterViewPostTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.organization = factories.Organization()
        factories.Group(name=ROLE_VIEW_ONLY)
        logging.disable(logging.ERROR)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    @staticmethod
    def _hotfix_django_bug(request):
        # Django 1.4 bug
        # https://code.djangoproject.com/ticket/17971
        from django.contrib.messages.storage.fallback import FallbackStorage
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

    def test_post_organization_not_found(self):
        data = {
            'org': 'Invalid Org'
        }
        request = self.factory.post(reverse('register'), data)
        self._hotfix_django_bug(request)
        view = views.RegisterView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        template_content = response.content
        self.assertIn('The Organization was not found',
                      template_content)

    def test_post_fields_not_sent(self):
        data = {
            'org': self.organization.name
        }
        request = self.factory.post(reverse('register'), data)
        self._hotfix_django_bug(request)
        view = views.RegisterView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        template_content = response.content
        for field in ('username', 'password1', 'password2',
                      'privacy_disclaimer_accepted'):
            msg = ('<p id="error_1_id_{}" class="help-block"><strong>'
                   'This field is required.</strong></p>'.format(field))
            self.assertIn(msg, template_content)

    @patch('tola.track_sync.requests')
    def test_post_success_with_full_name(self, mock_requests):
        mock_requests.post.return_value = Mock(status_code=201)

        data = {
            'first_name': 'John',
            'last_name': 'Lennon',
            'email': 'johnlennon@test.com',
            'username': 'ILoveYoko',
            'password1': '123456',
            'password2': '123456',
            'title': TITLE_CHOICES[0][0],
            'privacy_disclaimer_accepted': 'on',
            'org': self.organization.name,
        }
        request = self.factory.post(reverse('register'), data)
        self._hotfix_django_bug(request)
        view = views.RegisterView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('index'), response.url)

        tolauser = TolaUser.objects.select_related('user').get(
            name='John Lennon')
        user = tolauser.user
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(tolauser.organization, self.organization)
        self.assertEqual(tolauser.title, data['title'])
        self.assertTrue(User.objects.filter(username='ILoveYoko').exists())

    @patch('tola.track_sync.requests')
    def test_post_success_with_first_name(self, mock_requests):
        mock_requests.post.return_value = Mock(status_code=201)

        data = {
            'first_name': 'John',
            'email': 'johnlennon@test.com',
            'username': 'ILoveYoko',
            'password1': '123456',
            'password2': '123456',
            'title': TITLE_CHOICES[0][0],
            'privacy_disclaimer_accepted': 'on',
            'org': self.organization.name,
        }
        request = self.factory.post(reverse('register'), data)
        self._hotfix_django_bug(request)
        view = views.RegisterView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('index'), response.url)

        tolauser = TolaUser.objects.select_related('user').get(
            name='John')
        user = tolauser.user
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(tolauser.organization, self.organization)
        self.assertEqual(tolauser.title, data['title'])
        self.assertTrue(User.objects.filter(username='ILoveYoko').exists())

    @patch('tola.track_sync.requests')
    def test_post_success_with_default_org(self, mock_requests):
        mock_requests.post.return_value = Mock(status_code=201)
        factories.Organization(name=settings.DEFAULT_ORG)
        os.environ['APP_BRANCH'] = DEMO_BRANCH

        data = {
            'first_name': 'John',
            'last_name': 'Lennon',
            'email': 'johnlennon@test.com',
            'username': 'ILoveYoko',
            'password1': '123456',
            'password2': '123456',
            'title': TITLE_CHOICES[0][0],
            'privacy_disclaimer_accepted': 'on',
        }
        request = self.factory.post(reverse('register'), data)
        self._hotfix_django_bug(request)
        view = views.RegisterView.as_view()
        response = view(request)
        os.environ['APP_BRANCH'] = ''
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('index'), response.url)

        tolauser = TolaUser.objects.select_related('user').get(
            name='John Lennon')
        user = tolauser.user
        self.assertEqual(user.first_name, data['first_name'])
        self.assertEqual(user.last_name, data['last_name'])
        self.assertEqual(user.email, data['email'])
        self.assertEqual(tolauser.organization.name, settings.DEFAULT_ORG)
        self.assertEqual(tolauser.title, data['title'])
        self.assertTrue(User.objects.filter(username='ILoveYoko').exists())

        os.environ['APP_BRANCH'] = ''


class TolaTrackSiloProxyTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.tola_user = factories.TolaUser()

    def test_get_unauthenticated_user(self):
        request = self.factory.get('')
        view = views.TolaTrackSiloProxy.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 403)

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('tola.views.requests')
    def test_get_authenticated_user_url_without_ending_slash(
            self, mock_requests):
        external_response = ['foo', {'bar': 'baz'}]
        mock_requests.get.return_value = Mock(
            status_code=200, content=json.dumps(external_response))
        request = Mock(user=self.tola_user.user)
        response = views.TolaTrackSiloProxy().get(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), external_response)
        mock_requests.get.assert_called_once_with(
            'https://tolatrack.com/api/silo?user_uuid={}'.format(
                self.tola_user.tola_user_uuid),
            headers={'content-type': 'application/json',
                     'Authorization': 'Token TheToken'})

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com/')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('tola.views.requests')
    def test_get_authenticated_user_url_with_ending_slash(
            self, mock_requests):
        external_response = ['foo', {'bar': 'baz'}]
        mock_requests.get.return_value = Mock(
            status_code=200, content=json.dumps(external_response))
        request = Mock(user=self.tola_user.user)
        response = views.TolaTrackSiloProxy().get(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), external_response)
        mock_requests.get.assert_called_once_with(
            'https://tolatrack.com/api/silo?user_uuid={}'.format(
                self.tola_user.tola_user_uuid),
            headers={'content-type': 'application/json',
                     'Authorization': 'Token TheToken'})

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com/')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('tola.views.requests')
    def test_get_gateway_502_exception(
            self, mock_requests):
        mock_requests.get.return_value = Mock(status_code=400)
        request = Mock(user=self.tola_user.user)
        response = views.TolaTrackSiloProxy().get(request)
        self.assertEqual(response.status_code, 502)


class TolaTrackSiloDataProxyTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.tola_user = factories.TolaUser()

    def test_get_unauthenticated_user(self):
        request = self.factory.get('')
        view = views.TolaTrackSiloDataProxy.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 403)

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('tola.views.requests')
    def test_get_authenticated_user_url_without_ending_slash(
            self, mock_requests):
        external_response = ['foo', {'bar': 'baz'}]
        mock_requests.get.return_value = Mock(
            status_code=200, content=json.dumps(external_response))
        request = Mock(user=self.tola_user.user)
        response = views.TolaTrackSiloDataProxy().get(request, '123')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), external_response)
        mock_requests.get.assert_called_once_with(
            'https://tolatrack.com/api/silo/123/data',
            headers={'content-type': 'application/json',
                     'Authorization': 'Token TheToken'})

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com/')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('tola.views.requests')
    def test_get_authenticated_user_url_with_ending_slash(
            self, mock_requests):
        external_response = ['foo', {'bar': 'baz'}]
        mock_requests.get.return_value = Mock(
            status_code=200, content=json.dumps(external_response))
        request = Mock(user=self.tola_user.user)
        response = views.TolaTrackSiloDataProxy().get(request, '123')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), external_response)
        mock_requests.get.assert_called_once_with(
            'https://tolatrack.com/api/silo/123/data',
            headers={'content-type': 'application/json',
                     'Authorization': 'Token TheToken'})

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com/')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('tola.views.requests')
    def test_get_gateway_502_exception(
            self, mock_requests):
        mock_requests.get.return_value = Mock(status_code=400)
        request = Mock(user=self.tola_user.user)
        response = views.TolaTrackSiloDataProxy().get(request, '288')
        self.assertEqual(response.status_code, 502)


class LogoutViewTest(TestCase):
    def setUp(self):
        self.user = factories.User()
        self.user.set_password(12345)
        self.user.save()
        self.tola_user = factories.TolaUser(user=self.user)
        self.factory = RequestFactory()

    def test_logout_redirect_to_track(self):
        c = Client()
        c.post('/accounts/login/', {'username': self.user.username,
                                    'password': '12345'})
        self.user = auth.get_user(c)
        self.assertEqual(self.user.is_authenticated(), True)

        response = c.post('/accounts/logout/')
        self.user = auth.get_user(c)
        self.assertEqual(self.user.is_authenticated(), False)
        self.assertEqual(response.status_code, 302)

        url_subpath = 'accounts/logout/'
        redirect_url = urljoin(settings.TOLA_TRACK_URL, url_subpath)
        self.assertEqual(response.url, redirect_url)

    def test_logout_redirect_to_index(self):
        c = Client()
        response = c.post('/accounts/logout/')
        self.user = auth.get_user(c)
        self.assertEqual(self.user.is_authenticated(), False)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
