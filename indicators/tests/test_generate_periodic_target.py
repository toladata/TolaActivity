import datetime

from django.test import TestCase

from indicators.models import Indicator
from indicators.views import generate_periodic_target_single


class GeneratePeriodicTargetTests(TestCase):

    def setUp(self):
        self.start_date = datetime.datetime.now()
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
