from django.test import TestCase

from TolaActivity.factories import UserFactory
from indicators.views import group_excluded


class GroupExcluded(TestCase):

    def test_kickout_non_authed(self):
        """It should return false if the user is not authenticated"""
        user = UserFactory(first_name="Test", last_name="kicked")
        result = group_excluded("")

    def test_user_not_in_groups(self):
        """"
        It should return true if the user is NOT in any of the named groups
        """
        user = UserFactory(first_name="Test", last_name="Accepted")

    def test_user_in_group(self):
        """
        It should raise a PermissionDenied exception if the user is in ANY of
        the named groups
        """
        user = UserFactory(first_name="Test", last_name="Raises")
