# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings, tag

import factories
from workflow.models import (Dashboard, TolaUser, Office,
                             ROLE_ORGANIZATION_ADMIN)


@tag('pkg')
class DashboardTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()

    def test_save_without_public_info(self):
        custom_form = Dashboard(
            user=self.tola_user,
            name="Humanitec's Dashboard",
            public={}
        )
        self.assertRaises(ValidationError, custom_form.save)

    def test_save_without_public_org_info(self):
        custom_form = Dashboard(
            user=self.tola_user,
            name="Humanitec's Dashboard",
            public={'url': True}
        )
        self.assertRaises(ValidationError, custom_form.save)

    def test_save_without_public_url_info(self):
        custom_form = Dashboard(
            user=self.tola_user,
            name="Humanitec's Dashboard",
            public={'org': True}
        )
        self.assertRaises(ValidationError, custom_form.save)

    def test_save_without_public_all_info(self):
        custom_form = Dashboard(
            user=self.tola_user,
            name="Humanitec's Dashboard",
            public={'org': True, 'url': True}
        )
        self.assertRaises(ValidationError, custom_form.save)

    def test_save_with_public_info(self):
        custom_form = Dashboard.objects.create(
            user=self.tola_user,
            name="Humanitec's Dashboard",
            public={'all': False, 'org': True, 'url': True}
        )
        self.assertEqual(custom_form.name, "Humanitec's Dashboard")
        self.assertEqual(custom_form.public,
                         {'all': False, 'org': True, 'url': True})


@tag('pkg')
class TolaUserTest(TestCase):
    def setUp(self):
        self.organization = factories.Organization()
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

    def test_save_role_org_admin_fails(self):
        wfteam = factories.WorkflowTeam.build(
            role=factories.Group(name=ROLE_ORGANIZATION_ADMIN),
            workflow_user=factories.TolaUser(),
            workflowlevel1=factories.WorkflowLevel1())
        self.assertRaises(ValidationError, wfteam.save)


@tag('pkg')
class ProductTest(TestCase):
    def test_print_instance(self):
        product = factories.Product()
        self.assertEqual(unicode(product), u'Próduct P <Help Syrians>')


@tag('pkg')
class OfficeTest(TestCase):
    def test_print_instance(self):
        office = Office(name="Office", code="Code")
        self.assertEqual(unicode(office), u'Office - Code')

    def test_print_instance_without_code(self):
        office = Office(name="Office", code=None)
        self.assertEqual(unicode(office), u'Office')


@tag('pkg')
class WorkflowLevel1Test(TestCase):
    def test_print_instance_no_org(self):
        wflvl1 = factories.WorkflowLevel1.build(name='ACME', organization=None)
        self.assertEqual(unicode(wflvl1), u'ACME')

    def test_print_instance_with_org(self):
        organization = factories.Organization(name='ACME Org')
        wflvl1 = factories.WorkflowLevel1.build(name='ACME',
                                                organization=organization)
        self.assertEqual(unicode(wflvl1), u'ACME <ACME Org>')


@tag('pkg')
class WorkflowLevel2Test(TestCase):
    def test_print_instance(self):
        wflvl2 = factories.WorkflowLevel2.build()
        self.assertEqual(unicode(wflvl2), u'Help Syrians')

    def test_save_address_fail(self):
        wflvl2 = factories.WorkflowLevel2()
        wflvl2.address = {
            'street': None,
        }
        self.assertRaises(ValidationError, wflvl2.save)

        wflvl2.address = {
            'house_number': 'a'*21,
        }
        self.assertRaises(ValidationError, wflvl2.save)

    def test_save_address(self):
        factories.WorkflowLevel2(address={
            'street': 'Oderberger Straße',
            'house_number': '16A',
            'postal_code': '10435',
            'city': 'Berlin',
            'country': 'Germany',
        })


@tag('pkg')
class OrganizationTest(TestCase):
    def test_print_instance(self):
        organization = factories.Organization.build()
        self.assertEqual(unicode(organization), u'Tola Org')

    def test_save_phone(self):
        organization = factories.Organization(phone="+49 123 456 111")
        self.assertEqual(organization.phone, "+49 123 456 111")

    def test_save_organization_with_siteprofile(self):
        country = factories.Country(country='Germany')
        siteprofile = factories.SiteProfile(name='Headquarter',
                                            country=country)
        organization = factories.Organization(site=siteprofile)
        self.assertEqual(organization.site.name, 'Headquarter')
