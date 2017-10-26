# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from docs.api.Connection import TolaApiConnection
from tola.settings.local import *
from django.test import Client
from django.contrib.auth.models import User
from oauth2_provider.models import Application

# TODO Extend OAuth tests


class OAuthTest(TestCase):
    """
    Test cases for OAuth Provider interface
    """

    fixtures = ['fixtures/users.json','fixtures/oauth_test_data.json']

    def test_authorization(self):
        """
        Tests if the simple search responds
        :return: 
        """
        c = Client(HTTP_USER_AGENT='Test/1.0')
        c.login(username='test', password='1234')

        oauth_app = Application.objects.all()[0]

        #Get Authorization token
        authorize_url = '/oauth/authorize?state=random_state_string' \
                        '&client_id='+oauth_app.client_id+'' \
                        '&response_type=code'

        response = c.get(authorize_url, follow=True)

        self.assertContains(response, "value=\"CXGVOGFnTAt5cQW6m5AxbGrRq1lzKNSrou31dWm9\"")
        self.assertEqual(response.status_code, 200)
