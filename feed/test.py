"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from docs.api.Connection import TolaApiConnection
from tola.settings.local import *
from django.test import Client
from django.contrib.auth.models import User

class SimpleTest(TestCase):
    @classmethod
    def setUp(cls):
        user = User.objects.create_user('test', 'test@example.com', 'testpass')
        user.save()

    def test_login_redirect(self):
        c = Client(HTTP_USER_AGENT='Test/1.0')
        response = c.get('/login/', follow=True)

        self.assertRedirects(response, '/accounts/login/?next=/login/')
        self.assertEqual(response.status_code, 200)

    def test_user_login(self):
        """
        Tests if the user login works and a logged in user doesnt get redirected
        :return: 
        """
        c = Client(HTTP_USER_AGENT='Test/1.0')
        c.login(username='test', password='testpass')
        response = c.get('/workflow/dashboard/0/', follow=True)

        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.status_code, 200)

    def test_access_control(self):
        """
        Tests if the access control works
        :return: 
        """
        c = Client(HTTP_USER_AGENT='Test/1.0')
        response = c.get('/indicators/home/0/0/0/', follow=True)

        print(response.redirect_chain, response.status_code)
        print(response.context)

        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.status_code, 200)

        c.login(username='test', password='testpass')

        response = c.get('/indicators/home/0/0/0/', follow=True)

        print(response.redirect_chain, response.status_code)
        print(response.context)
        print(response)

        self.assertEqual(len(response.redirect_chain), 0)
        self.assertEqual(response.status_code, 200)
