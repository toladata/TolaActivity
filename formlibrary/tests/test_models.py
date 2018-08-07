# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError
from django.test import TestCase, tag

import factories
from formlibrary.models import CustomForm


@tag('pkg')
class CustomFormTest(TestCase):
    def setUp(self):
        self.organization = factories.Organization()
        self.user = factories.User()

    def test_save_without_public_info(self):
        custom_form = CustomForm(
            organization=self.organization,
            name="Humanitec's Survey",
            fields="{}",
            public={}
        )

        self.assertRaises(ValidationError, custom_form.save)

    def test_save_without_public_org_info(self):
        custom_form = CustomForm(
            organization=self.organization,
            name="Humanitec's Survey",
            fields="{}",
            public={'url': True}
        )

        self.assertRaises(ValidationError, custom_form.save)

    def test_save_without_public_url_info(self):
        custom_form = CustomForm(
            organization=self.organization,
            name="Humanitec's Survey",
            fields="{}",
            public={'org': True}
        )

        self.assertRaises(ValidationError, custom_form.save)

    def test_save_with_public_info(self):
        custom_form = CustomForm.objects.create(
            organization=self.organization,
            name="Humanitec's Survey",
            fields="{}",
            public={'org': True, 'url': True}
        )

        self.assertEqual(custom_form.name, "Humanitec's Survey")
        self.assertEqual(custom_form.public, {'org': True, 'url': True})
