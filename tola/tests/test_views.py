import json

from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase, override_settings
from mock import Mock, patch

import factories
from tola import views
from workflow.models import TolaUser, ROLE_VIEW_ONLY

# TODO Extend View tests


class ViewsTest(TestCase):
    """
    Test cases for Views
    """
    def setUp(self):
        site = Site.objects.create(name='TolaSite')
        factories.TolaSites(site=site)
        factories.Group(name=ROLE_VIEW_ONLY)

        self.org = factories.Organization()
        self.factory = RequestFactory()

    def test_register_full_name(self):
        data = {
            'first_name': 'John',
            'last_name': 'Lennon',
            'email': 'johnlennon@test.com',
            'username': 'johnlennon',
            'password1': 'thebeatles',
            'password2': 'thebeatles',
            'title': '',
            'privacy_disclaimer_accepted': 'on',
            'org': self.org.name
        }

        request = self.factory.post('/accounts/register/', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = views.register(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/')

        tolauser = TolaUser.objects.filter(name='John Lennon')
        user = User.objects.filter(username='johnlennon')
        self.assertEqual(len(tolauser), 1)
        self.assertEqual(len(user), 1)

    def test_register_first_name(self):
        data = {
            'first_name': 'John',
            'email': 'johnlennon@test.com',
            'username': 'johnlennon',
            'password1': 'thebeatles',
            'password2': 'thebeatles',
            'title': '',
            'privacy_disclaimer_accepted': 'on',
            'org': self.org.name
        }

        request = self.factory.post('/accounts/register/', data)
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        response = views.register(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/')

        tolauser = TolaUser.objects.filter(name='John')
        user = User.objects.filter(username='johnlennon')
        self.assertEqual(len(tolauser), 1)
        self.assertEqual(len(user), 1)


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