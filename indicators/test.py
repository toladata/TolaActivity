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
        """
        Create a couple indicators and a program
        """
        self.program = factories.Program()
        self.indicators = factories.RandomIndicatorFactory.create_batch(
            2, program=self.program, source="TEST")
        self.tola_user = factories.TolaUser()

    def test_indicator_exists(self):
        self.assertEqual(Indicator.objects.count(), 2)

    def test_program_exist(self):
        self.assertEqual(Program.objects.count(), 1)

    def test_collected_data_json_view(self):
        """
        Tests summary values are accurate for various configurations of an
        Indicator
        """
        indicator = factories.Indicator.create(
            program=self.program, source="TEST2")

        url = reverse('collected_data_json',
                      kwargs={
                        'indicator': indicator.id,
                        'program': self.program.id
                        })
        response = self.client.get(url)
        self.assertEqual(0, response.context['grand_achieved_sum'])

    def ztest_collected_exists(self):
        """
        Check for CollectedData object
        """
        indicatorDataRecord = CollectedData.objects.get(
            description="somevaluecollected")

        self.assertEqual(CollectedData.objects.filter(
            id=indicatorDataRecord.id).count(), 1)
