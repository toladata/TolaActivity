from django.test import TestCase, override_settings, tag

import factories
from workflow.models import TolaUser, Office


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
        tolauser = factories.TolaUser.build(name=None)
        self.assertEqual(unicode(tolauser), u'-')

    def test_print_instance_empty_name(self):
        tolauser = factories.TolaUser.build(name='')
        self.assertEqual(unicode(tolauser), u'-')

    def test_print_instance_name(self):
        tolauser = factories.TolaUser.build(name='Daniel Avery')
        self.assertEqual(unicode(tolauser), u'Daniel Avery')

    @override_settings(TOLAUSER_OBFUSCATED_NAME='Fake Name')
    def test_print_instance_with_obfuscated_name_and_fallback(self):
        tolauser = factories.TolaUser.build()
        self.assertEqual(unicode(tolauser), u'Thom Yorke')

    @override_settings(TOLAUSER_OBFUSCATED_NAME='Fake Name')
    def test_print_instance_with_obfuscated_name_without_fallback(self):
        user = factories.User(first_name='', last_name='')
        tolauser = factories.TolaUser(user=user)
        self.assertEqual(unicode(tolauser), u'-')


@tag('pkg')
class WorkflowTeamTest(TestCase):
    def test_print_instance(self):
        wfteam = factories.WorkflowTeam()
        self.assertEqual(unicode(wfteam),
                         (u'Thom Yorke - ProgramAdmin <Health and Survival '
                          u'for Syrians in Affected Regions>'))


@tag('pkg')
class OfficeTest(TestCase):
    def test_print_instance(self):
        office = Office(name="Office", code="Code")
        self.assertEqual(unicode(office), u'Office - Code')

    def test_print_instance_without_code(self):
        office = Office(name="Office", code=None)
        self.assertEqual(unicode(office), u'Office')



@tag('pkg')
class ContactTest(TestCase):
    def test_print_instance(self):
        contact = factories.Contact.build(title="Title")
        self.assertEqual(unicode(contact), u'Aryana Sayeed, Title')

    def test_print_instance_without_title(self):
        contact = factories.Contact.build()
        self.assertEqual(unicode(contact), u'Aryana Sayeed')


@tag('pkg')
class WorkflowLevel2Test(TestCase):
    def test_print_instance(self):
        wflvl2 = factories.WorkflowLevel2.build()
        self.assertEqual(unicode(wflvl2), u'Help Syrians')
