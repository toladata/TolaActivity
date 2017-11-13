# -*- coding: utf-8 -*-
import factories

from django.test import TestCase
from django.http import HttpResponse
from workflow.models import TolaUser
from tola import util

# TODO Extend Util tests


class UtilTest(TestCase):
    """
    Test cases for Utils interface
    """
    def setUp(self):
        self.org = factories.Organization()
        self.country = factories.Country()

    def test_user_to_tola(self):
        # TolaUser will be create with default Org
        response = {
            'displayName': 'Foo Bar',
            'emails': [{
                'type': 'account',
                'value': 'foo@bar.com'
            }]
        }
        user = factories.User.build(is_superuser=True, is_staff=True)
        user.save()

        util.user_to_tola(None, user, response)
        tola_user = TolaUser.objects.get(user=user)

        self.assertEqual(tola_user.name, response.get('displayName'))
        self.assertEqual(tola_user.organization.name, self.org.name)
        self.assertEqual(tola_user.country.country, self.country.country)

        # TolaUser will be retrieved and Org won't be the default anymore
        new_org = factories.Organization(name='New Organization')
        tola_user.organization = new_org
        tola_user.save()
        util.user_to_tola(None, user, response)
        tola_user = TolaUser.objects.get(user=user)

        self.assertEqual(tola_user.organization.name, new_org.name)
