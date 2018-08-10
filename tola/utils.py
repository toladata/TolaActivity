# -*- coding: utf-8 -*-
import logging
from datetime import date

from django.utils import six
from django.utils.crypto import constant_time_compare, salted_hmac
from django.utils.http import base36_to_int, int_to_base36

logger = logging.getLogger(__name__)


class TokenGenerator(object):
    """
    Strategy object used to generate and check tokens for public URLs.
    """
    key_salt = "web.utils.TokenGenerator"

    def make_token(self, instance, flag=None):
        """
        Returns a token that can be used to access an object.
        """
        return self._make_token_with_timestamp(
            instance, self._num_days(self._today()), flag)

    def check_token(self, instance, token, flag=None):
        """
        Check that a token is correct for a given object and the object is
        really set as public.
        """
        if not (instance and token):
            return False

        is_public = self._get_attr_by_suffix(instance, 'public')
        if not is_public:
            return False
        # Parse the token
        try:
            ts_b36, hash = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(
                self._make_token_with_timestamp(
                    instance, ts, flag), token):
            return False

        return True

    def _make_token_with_timestamp(self, instance, timestamp, flag=None):
        # timestamp is number of days since 2001-1-1.  Converted to
        # base 36, this gives us a 3 digit string until about 2121
        ts_b36 = int_to_base36(timestamp)

        # By hashing on the internal state of the instance and using state
        # that is sure to change (the public salt will change as soon as
        # the public field is changed)
        # We limit the hash to 20 chars to keep URL short
        hash = salted_hmac(
            self.key_salt,
            self._make_hash_value(instance, timestamp, flag),
        ).hexdigest()[::2]
        return '{}-{}'.format(ts_b36, hash)

    def _make_hash_value(self, instance, timestamp, flag=None):
        # Ensure results are consistent across DB backends
        attr = self._get_attr_by_suffix(instance, 'uuid')
        attr = attr if attr else instance.__class__.__name__

        return (
            six.text_type(flag if flag is not None else instance.pk) +
            six.text_type(attr) + six.text_type(timestamp)
        )

    def _get_attr_by_suffix(self, instance, suffix):
        attributes = instance.__dict__.keys()
        for attr in attributes:
            if attr.endswith(suffix):
                return instance.__getattribute__(attr)

        return None

    def _num_days(self, dt):
        return (dt - date(2001, 1, 1)).days

    def _today(self):
        # Used for mocking in tests
        return date.today()
