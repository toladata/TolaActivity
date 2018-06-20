# -*- coding: utf-8 -*-
from django.test import TestCase, tag
from django.utils import six
from django.utils.crypto import salted_hmac
from django.utils.http import int_to_base36

import factories
from workflow.models import Dashboard
from .. import utils


@tag('pkg')
class TokenGeneratorTest(TestCase):
    def setUp(self):
        self.token_generator = utils.TokenGenerator()

    def test_get_attr_by_suffix_exist(self):
        tola_user = factories.TolaUser()

        attr = self.token_generator._get_attr_by_suffix(tola_user, 'name')
        self.assertEqual(attr, tola_user.name)

    def test_get_attr_by_suffix_not_exist(self):
        tola_user = factories.TolaUser()

        attr = self.token_generator._get_attr_by_suffix(tola_user, 'test')
        self.assertIsNone(attr)

    def test_make_hash_value_with_uuid_and_no_flag(self):
        tola_user = factories.TolaUser()
        create_date = tola_user.create_date.replace(
            microsecond=0, tzinfo=None)
        timestamp = self.token_generator._num_days(
            self.token_generator._today())

        expected_hash = (
            six.text_type(tola_user.pk) + tola_user.tola_user_uuid.__str__() +
            six.text_type(create_date) + six.text_type(timestamp)
        )

        generated_hash = self.token_generator._make_hash_value(
            tola_user, timestamp)
        self.assertEqual(generated_hash, expected_hash)

    def test_make_hash_value_with_uuid_and_flag(self):
        tola_user = factories.TolaUser()
        create_date = tola_user.create_date.replace(
            microsecond=0, tzinfo=None)
        timestamp = self.token_generator._num_days(
            self.token_generator._today())

        expected_hash = (
            six.text_type(True) + tola_user.tola_user_uuid.__str__() +
            six.text_type(create_date) + six.text_type(timestamp)
        )

        generated_hash = self.token_generator._make_hash_value(
            tola_user, timestamp, flag=True)
        self.assertEqual(generated_hash, expected_hash)

    def test_make_token_with_timestamp(self):
        tola_user = factories.TolaUser()
        create_date = tola_user.create_date.replace(
            microsecond=0, tzinfo=None)
        timestamp = self.token_generator._num_days(
            self.token_generator._today())

        test_hash = (
            six.text_type(True) + tola_user.tola_user_uuid.__str__() +
            six.text_type(create_date) + six.text_type(timestamp)
        )

        ts_b36 = int_to_base36(timestamp)
        hash = salted_hmac(self.token_generator.key_salt,
                           test_hash).hexdigest()[::2]

        generated_hash = self.token_generator._make_token_with_timestamp(
            tola_user, timestamp, flag=True)
        self.assertEqual(generated_hash, '{}-{}'.format(ts_b36, hash))

    def test_check_token_no_public_attribute(self):
        tola_user = factories.TolaUser()

        with self.assertRaises(AttributeError) as context:
            self.token_generator.check_token(tola_user, 'TokenTest')
            self.assertTrue('\'dict\' object has no attribute \'test\''
                            in context.exception)

    def test_check_token_token_is_none(self):
        tola_user = factories.TolaUser()
        is_valid = self.token_generator.check_token(tola_user, None)
        self.assertFalse(is_valid)

    def test_check_token_instance_is_none(self):
        is_valid = self.token_generator.check_token(None, 'TokenTest')
        self.assertFalse(is_valid)

    def test_check_token_token_wrong_format(self):
        dashboard = factories.Dashboard(public=Dashboard.PUBLIC_URL)
        create_date = dashboard.create_date.replace(
            microsecond=0, tzinfo=None)
        timestamp = self.token_generator._num_days(
            self.token_generator._today())

        test_hash = (
                six.text_type(dashboard.public) +
                dashboard.dashboard_uuid.__str__() +
                six.text_type(create_date) + six.text_type(timestamp)
        )

        ts_b36 = int_to_base36(timestamp)
        hash = salted_hmac(self.token_generator.key_salt,
                           test_hash).hexdigest()[::2]
        final_hash = '{}{}'.format(ts_b36, hash)

        is_valid = self.token_generator.check_token(dashboard, final_hash,
                                                    dashboard.public)
        self.assertFalse(is_valid)

    def test_check_token_invalid_timestamp_token(self):
        dashboard = factories.Dashboard(public=Dashboard.PUBLIC_URL)
        create_date = dashboard.create_date.replace(
            microsecond=0, tzinfo=None)
        timestamp = self.token_generator._num_days(
            self.token_generator._today())

        test_hash = (
                six.text_type(dashboard.public) +
                dashboard.dashboard_uuid.__str__() +
                six.text_type(create_date) + six.text_type(timestamp)
        )

        hash = salted_hmac(self.token_generator.key_salt,
                           test_hash).hexdigest()[::2]
        final_hash = '{}-{}'.format(timestamp, hash)

        is_valid = self.token_generator.check_token(dashboard, final_hash,
                                                    dashboard.public)
        self.assertFalse(is_valid)

    def test_check_token_no_public(self):
        dashboard = factories.Dashboard()
        create_date = dashboard.create_date.replace(
            microsecond=0, tzinfo=None)
        timestamp = self.token_generator._num_days(
            self.token_generator._today())

        test_hash = (
                six.text_type(dashboard.pk) +
                dashboard.dashboard_uuid.__str__() +
                six.text_type(create_date) + six.text_type(timestamp)
        )

        hash = salted_hmac(self.token_generator.key_salt,
                           test_hash).hexdigest()[::2]
        final_hash = '{}-{}'.format(timestamp, hash)

        is_valid = self.token_generator.check_token(dashboard, final_hash)
        self.assertFalse(is_valid)

    def test_check_token_invalid_token(self):
        dashboard = factories.Dashboard(public=Dashboard.PUBLIC_URL)
        create_date = dashboard.create_date.replace(
            microsecond=0, tzinfo=None)
        timestamp = self.token_generator._num_days(
            self.token_generator._today())

        test_hash = (
                six.text_type(True) + dashboard.dashboard_uuid.__str__() +
                six.text_type(create_date) + six.text_type(timestamp)
        )

        hash = salted_hmac(self.token_generator.key_salt,
                           test_hash).hexdigest()[::2]
        final_hash = '{}-{}'.format(timestamp, hash)

        is_valid = self.token_generator.check_token(dashboard, final_hash)
        self.assertFalse(is_valid)

    def test_check_token_success_with_flag(self):
        dashboard = factories.Dashboard(public=Dashboard.PUBLIC_URL)
        create_date = dashboard.create_date.replace(
            microsecond=0, tzinfo=None)
        timestamp = self.token_generator._num_days(
            self.token_generator._today())

        test_hash = (
                six.text_type(dashboard.public) +
                dashboard.dashboard_uuid.__str__() +
                six.text_type(create_date) + six.text_type(timestamp)
        )

        ts_b36 = int_to_base36(timestamp)
        hash = salted_hmac(self.token_generator.key_salt,
                           test_hash).hexdigest()[::2]
        final_hash = '{}-{}'.format(ts_b36, hash)

        is_valid = self.token_generator.check_token(
            dashboard, final_hash, dashboard.public)
        self.assertTrue(is_valid)

    def test_check_token_success_without_flag(self):
        dashboard = factories.Dashboard(public=Dashboard.PUBLIC_URL)
        create_date = dashboard.create_date.replace(
            microsecond=0, tzinfo=None)
        timestamp = self.token_generator._num_days(
            self.token_generator._today())

        test_hash = (
                six.text_type(dashboard.pk) +
                dashboard.dashboard_uuid.__str__() +
                six.text_type(create_date) + six.text_type(timestamp)
        )

        ts_b36 = int_to_base36(timestamp)
        hash = salted_hmac(self.token_generator.key_salt,
                           test_hash).hexdigest()[::2]
        final_hash = '{}-{}'.format(ts_b36, hash)

        is_valid = self.token_generator.check_token(dashboard, final_hash)
        self.assertTrue(is_valid)
