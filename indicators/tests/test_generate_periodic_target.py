import datetime

from django.test import TestCase

from indicators.models import Indicator
from indicators.views.views_indicators import generate_periodic_target_single, \
    generate_periodic_targets


class GeneratePeriodicTargetTests(TestCase):

    def setUp(self):
        self.start_date = datetime.datetime(2018, 10, 5, 18, 00)
        self.nth_target_period = 10
        self.target_frequency_custom = 5

    def test_lop_generate_periodic_target_single(self):
        """Do we get back the expected result when we have an LOP?"""
        tf = Indicator.LOP
        expected = {'period': "Life of Program (LoP) only"}
        result = generate_periodic_target_single(tf, self.start_date,
                                                 self.nth_target_period,
                                                 target_frequency_custom=self.target_frequency_custom)
        self.assertDictEqual(expected, result)

    def test_mid_generate_periodic_target_single(self):
        """Do we get back the expected result when we have an MID_END?"""
        tf = Indicator.MID_END
        expected = [{'period': 'Midline'}, {'period': 'Endline'}]
        result = generate_periodic_target_single(tf, self.start_date,
                                                 self.nth_target_period,
                                                 target_frequency_custom=self.target_frequency_custom)
        self.assertEqual(expected, result)

    def test_event_generate_periodic_target_single(self):
        """Do we get back the expected result when we have an EVENT?"""
        tf = Indicator.EVENT
        expected = {'period': self.target_frequency_custom}
        result = generate_periodic_target_single(tf, self.start_date,
                                                 self.nth_target_period,
                                                 target_frequency_custom=self.target_frequency_custom)
        self.assertEqual(expected, result)

    def test_annual(self):
        """Do we get back the correct value if it is ANNUAL"""

        tf = Indicator.ANNUAL
        # TODO: Get clarification on the business rules for this function
        expected = {'period': 'Year 11', 'end_date': '2029-10-04',
                    'start_date': '2028-10-01'}

        result = generate_periodic_target_single(tf, self.start_date,
                                                 self.nth_target_period,
                                        target_frequency_custom='')
        self.assertDictEqual(expected, result)

    def test_semi_annual(self):
        tf = Indicator.SEMI_ANNUAL

        # TODO: Get clarification on the business rules for this function
        expected = {'end_date': '2024-04-04',
                    'period': 'Semi-annual period 11',
                    'start_date': '2023-10-01'}

        result = generate_periodic_target_single(tf, self.start_date,
                                                 self.nth_target_period,
                                                 target_frequency_custom='')
        self.assertDictEqual(expected, result)

    def test_tri_annual(self):
        tf = Indicator.TRI_ANNUAL
        # TODO: Get clarification on the business rules for this function
        expected = {'end_date': '2022-06-04',
                    'period': 'Tri-annual period 11',
                    'start_date': '2022-02-01'}

        result = generate_periodic_target_single(tf, self.start_date,
                                                 self.nth_target_period,
                                                 target_frequency_custom='')
        self.assertDictEqual(expected, result)

    def test_quarterly(self):
        tf = Indicator.QUARTERLY

        # TODO: Get clarification on the business rules for this function
        expected = {'end_date': '2021-07-04', 
                    'period': 'Quarter 11', 
                    'start_date': '2021-04-01'}

        result = generate_periodic_target_single(tf, self.start_date,
                                                 self.nth_target_period,
                                                 target_frequency_custom='')
        self.assertDictEqual(expected, result)

    def test_monthly(self):
        tf = Indicator.MONTHLY

        # TODO: Get clarification on the business rules for this function
        expected = {'end_date': '2019-09-04',
                    'period': 'August 2019',
                    'start_date': '2019-08-01'}

        result = generate_periodic_target_single(tf, self.start_date,
                                                 self.nth_target_period,
                                        target_frequency_custom='')
        self.assertDictEqual(expected, result)


class GenerateTargetsTests(TestCase):

    def setUp(self):
        self.start_date = datetime.datetime(2018, 10, 5, 18, 00)
        self.total_targets = 10
        self.target_frequency_custom = ''

    def test_generate(self):
        """Can we bulk generate periodic targets?"""

        tf = Indicator.MONTHLY
        result = generate_periodic_targets(tf, self.start_date, self.total_targets,
                                           self.target_frequency_custom)

        self.assertTrue(len(result) == 10)

    def test_lop(self):
        """Do we get back the correct response if we are doing
        Life of Project?"""

        tf = Indicator.LOP
        expected = {'period': u'Life of Program (LoP) only'}
        result = generate_periodic_targets(tf, self.start_date,
                                           self.total_targets,
                                           self.target_frequency_custom)
        self.assertDictEqual(expected, result)

    def test_mid(self):
        """Do we get back the correct response if we are doing MID?"""

        tf = Indicator.MID_END
        expected = [{'period': 'Midline'}, {'period': 'Endline'}]
        result = generate_periodic_targets(tf, self.start_date,
                                           self.total_targets,
                                           self.target_frequency_custom)

        self.assertEqual(expected, result)