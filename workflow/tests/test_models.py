from django.test import TestCase, override_settings, tag

import factories
from workflow.models import TolaUser


@tag('pkg')
class TolaUserTest(TestCase):
    def setUp(self):
        self.organization =  factories.Organization()
        self.user = factories.User()

    @override_settings(TOLAUSER_OBFUSCATED_NAME='Fake Name')
    def test_save_obfuscated_name(self):
        tola_user = TolaUser.objects.create(name='Thom Yorke', user=self.user,
                                            organization=self.organization)
        self.assertEqual(tola_user.name, 'Fake Name')

    def test_save_without_obfuscated_name(self):
        tola_user = TolaUser.objects.create(name='Thom Yorke', user=self.user,
                                            organization=self.organization)
        self.assertEqual(tola_user.name, 'Thom Yorke')

    def test_print_instance_no_name(self):
        tolauser = factories.TolaUser(name=None)
        self.assertEqual(unicode(tolauser), u'-')

    def test_print_instance_empty_name(self):
        tolauser = factories.TolaUser(name='')
        self.assertEqual(unicode(tolauser), u'-')

    def test_print_instance_name(self):
        tolauser = factories.TolaUser(name='Daniel Avery')
        self.assertEqual(unicode(tolauser), u'Daniel Avery')

    @override_settings(TOLAUSER_OBFUSCATED_NAME='Fake Name')
    def test_print_instance_with_obfuscated_name_and_fallback(self):
        tolauser = factories.TolaUser()
        self.assertEqual(unicode(tolauser), u'Thom Yorke')

    @override_settings(TOLAUSER_OBFUSCATED_NAME='Fake Name')
    def test_print_instance_with_obfuscated_name_without_fallback(self):
        user = factories.User(first_name='', last_name='')
        tolauser = factories.TolaUser(user=user)
        self.assertEqual(unicode(tolauser), u'-')
