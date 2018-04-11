from django.urls import reverse
from django.test import TestCase
from django.test import RequestFactory
from django.test import Client
from django.contrib.auth.models import User
from indicators.models import (
    Indicator,
    IndicatorType,
    DisaggregationType,
    ReportingFrequency,
    CollectedData
)
from workflow.models import (
    Program,
    Country,
    Organization
)
import factories

class IndicatorTestCase(TestCase):

    def setUp(self):
        print(".............................%s............................" % 'insetup' )
        """
        Create a couple indicators and a program
        """
        self.client = Client()
        self.program = factories.Program()
        self.indicators = factories.RandomIndicatorFactory.create_batch(
            2, program=self.program, source="TEST")
        self.user = User.objects.create_user('joe', 'joe@example.org', 'mercy')
        self.indicator = factories.Indicator.create(
            program=self.program, source="TEST2")

    def test_indicator_exists(self):
        self.assertEqual(Indicator.objects.count(), 3)

    def test_program_exist(self):
        self.assertEqual(Program.objects.count(), 1)

    def test_collected_data_view(self):
        """
        Tests summary values are accurate for various configurations of an
        Indicator
        """
        indicator = factories.Indicator.create(
            program=self.program, source="TEST2")

        url = reverse('collected_data_view',
                      kwargs={
                        'indicator': indicator.id,
                        'program': self.program.id
                        })
        response = self.client.get(url)
        self.assertEqual(0, response.context['grand_achieved_sum'])

    def test_generate_periodic_targets(self):
        self.indicator.target_frequency = Indicator.ANNUAL
        self.indicator.save()
        data = {
            "program": "512", "level": "1", "number": "1.1.2", "indicator_type": "1",
            "unit_of_measure": "count", "unit_of_measure_type": "2",
            "lop_target": "44", "direction_of_change": "1", "baseline": "10", "baseline_na": "off",
            "target_frequency": "3", "target_frequency_start": "Apr 12, 2017",
            "target_frequency_custom": "",
            "target_frequency_num_periods": "3", "is_cumulative": "2",
            "means_of_verification": "",
            "periodic_targets": [
                {"id":0,"period":"Year 1","target":"7","start_date":"Apr 01, 2017","end_date":"Mar 31, 2018"},
                {"id":0,"period":"Year 2","target":"7","start_date":"Apr 01, 2018","end_date":"Mar 31, 2019"},
                {"id":0,"period":"Year 3","target":"7","start_date":"Apr 01, 2019","end_date":"Mar 31, 2020"}
            ]
        }
        is_loggedin = self.client.login(username='joe', password='mercy')
        res = self.client.post(reverse('indicator_update',
                                       kwargs={'pk': self.indicator.id}),data)
        self.assertEqual(res.status_code, 200)

    def ztest_collected_exists(self):
        """
        Check for CollectedData object
        """
        indicatorDataRecord = CollectedData.objects.get(
            description="somevaluecollected")

        self.assertEqual(CollectedData.objects.filter(
            id=indicatorDataRecord.id).count(), 1)


class IPTTReportQuickstartTestCase(TestCase):
    def test_view_is_responsive(self):
        """
        Make sure the view is response and URL is correct
        """
        response = self.client.get(reverse('iptt_quickstart'))
        self.assertEqual(response.status_code, 200)



