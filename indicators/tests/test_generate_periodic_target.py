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
        tf = Indicator.LOP
        expected = {'period': 1}
        result = generate_periodic_target_single(tf, self.start_date,
                                                 self.nth_target_period,
                                                 target_frequency_custom=self.target_frequency_custom)
        self.assertDictEqual(expected, result)

    def test_lop_generate_periodic_target_single(self):
        tf = Indicator.MID_END
        expected = [{'period': 'Midline'}, {'period': 'Endline'}]
        result = generate_periodic_target_single(tf, self.start_date,
                                                 self.nth_target_period,
                                                 target_frequency_custom=self.target_frequency_custom)
        self.assertEqual(expected, result)

    def test_lop_generate_periodic_target_single(self):
        tf = Indicator.EVENT
        expected = {'period': self.target_frequency_custom}
        result = generate_periodic_target_single(tf, self.start_date,
                                                 self.nth_target_period,
                                                 target_frequency_custom=self.target_frequency_custom)
        self.assertEqual(expected, result)
