from django.test import TestCase
from django.test import Client
from django.contrib.sites.shortcuts import get_current_site

from social_core.exceptions import AuthForbidden

from workflow.models import TolaUser
from tola import auth_pipeline

import factories

# TODO Extend OAuth tests


class OAuthTest(TestCase):
    """
    Test cases for OAuth Provider interface
    """

    def setUp(self):
        self.tola_user = factories.TolaUser()
        self.org = factories.Organization()
        self.country = factories.Country()
        self.site = factories.TolaSites(site=get_current_site(None),
                                        whitelisted_domains='testenv.com')
        self.app = factories.Application(user=self.tola_user.user)
        self.grant = factories.Grant(application=self.app,
                                     user=self.tola_user.user)

    def test_authorization(self):
        """
        Tests if the simple search responds
        :return:
        """
        self.tola_user.user.set_password('1234')
        self.tola_user.user.save()

        c = Client(HTTP_USER_AGENT='Test/1.0')
        c.login(username=self.tola_user.user.username, password='1234')

        # Get Authorization token
        authorize_url = '/oauth/authorize?state=random_state_string' \
                        '&client_id={}&response_type=code'.format(
                            self.app.client_id)

        response = c.get(authorize_url, follow=True)
        self.assertContains(
            response, "value=\"CXGVOGFnTAt5cQW6m5AxbGrRq1lzKNSrou31dWm9\"")
        self.assertEqual(response.status_code, 200)

    def test_user_to_tola(self):
        # TolaUser will be created with default Org
        response = {
            'displayName': 'Foo Bar',
            'emails': [{
                'type': 'account',
                'value': 'foo@bar.com'
            }]
        }
        user = factories.User(first_name='John', last_name='Lennon',
                              is_superuser=True, is_staff=True)

        auth_pipeline.user_to_tola(None, user, response)
        tola_user = TolaUser.objects.get(user=user)

        self.assertEqual(tola_user.name, response.get('displayName'))
        self.assertEqual(tola_user.organization.name, self.org.name)
        self.assertEqual(tola_user.country.country, self.country.country)

        # TolaUser will be retrieved and Org won't be the default anymore
        new_org = factories.Organization(name='New Organization')
        tola_user.organization = new_org
        tola_user.save()
        auth_pipeline.user_to_tola(None, user, response)
        tola_user = TolaUser.objects.get(user=user)

        self.assertEqual(tola_user.organization.name, new_org.name)

    def test_auth_allowed_in_whitelist(self):
        # Fake backend class for the test
        class BackendTest(object):
            def __init__(self):
                self.WHITELISTED_EMAILS = []
                self.WHITELISTED_DOMAINS = []

            def setting(self, name, default=None):
                return self.__dict__.get(name, default)

        backend = BackendTest()
        details = {'email': self.tola_user.user.email}
        auth_pipeline.auth_allowed(backend, details, None)

    def test_auth_allowed_not_in_whitelist(self):
        # Fake backend class for the test
        class BackendTest(object):
            def __init__(self):
                self.WHITELISTED_EMAILS = []
                self.WHITELISTED_DOMAINS = []

            def setting(self, name, default=None):
                return self.__dict__.get(name, default)

        backend = BackendTest()
        details = {'email': self.tola_user.user.email}
        self.site.whitelisted_domains = 'anotherdomain.com'
        self.site.save()
        with self.assertRaises(AuthForbidden):
            auth_pipeline.auth_allowed(backend, details, None)

    def test_auth_allowed_no_whitelist(self):
        # Fake backend class for the test
        class BackendTest(object):
            def __init__(self):
                self.WHITELISTED_EMAILS = []
                self.WHITELISTED_DOMAINS = []

            def setting(self, name, default=None):
                return self.__dict__.get(name, default)

        self.site.whitelisted_domains = None
        self.site.save()

        backend = BackendTest()
        details = {'email': self.tola_user.user.email}
        auth_pipeline.auth_allowed(backend, details, None)
