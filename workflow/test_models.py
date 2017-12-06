from django.test import TestCase, override_settings

import factories
from workflow.models import TolaUser


class TolaUserTest(TestCase):
    def setUp(self):
        self.organization =  factories.Organization()
        self.user = factories.User()

    @override_settings(TOLAUSER_OFUSCATED_NAME='Fake Name')
    def test_save_ofuscate_name(self):
        tola_user = TolaUser.objects.create(name='Thom Yorke', user=self.user,
                                            organization=self.organization)
        self.assertEqual(tola_user.name, 'Fake Name')

    def test_save_without_ofuscate_name(self):

        tola_user = TolaUser.objects.create(name='Thom Yorke', user=self.user,
                                            organization=self.organization)
        self.assertEqual(tola_user.name, 'Thom Yorke')
