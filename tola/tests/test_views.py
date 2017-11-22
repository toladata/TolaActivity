# -*- coding: utf-8 -*-
import factories

from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase

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
