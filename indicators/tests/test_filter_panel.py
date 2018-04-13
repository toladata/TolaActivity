from unittest import skip

from django.test import TestCase


@skip("test not implemented")
class FilterPanelTests(TestCase):

    def setUp(self):
        pass

    def test_filter_by_program(self):
        """It should only show indicators associated with a given program"""
        self.fail("test not implemented")

    def test_filter_show_all(self):
        """It should show all indicators for a given project"""
        self.fail("test not implemented")

    def test_filter_limit_by_number(self):
        """
        It should limit the number of indicators shown by a given positive
        int
        """
        self.fail("test not implemented")

    def test_filter_by_date(self):
        """It should show only the indicators that fall in a given date range"""
        self.fail("test not implemented")

    def test_filter_by_level(self):
        """It should show only indicatators of the selected level"""
        self.fail("test not implemented")

    def test_filter_by_type(self):
        """It should only show indicators of the selected type"""
        self.fail("test not implemented")

    def test_filter_by_sector(self):
        """It should only show indicators for the selected sector"""
        self.fail("test not implemented")

    def test_filter_by_site(self):
        """It should only show indicators for the selected site"""
        self.fail("test not implemented")

    def test_filter_by_indicator(self):
        """It should only show the indicators for the selected indicator"""
        self.fail("test not implemented")