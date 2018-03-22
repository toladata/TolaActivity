from django.test import TestCase
from django.test import RequestFactory
from django.test import Client
from indicators.models import Indicator, IndicatorType, DisaggregationType, ReportingFrequency, CollectedData
from workflow.models import Program, Country, Organization
from django.contrib.auth.models import User
from indicators.base_test_helper import populateDbWithTestData as dbSetup
import factories


class IndicatorTestCase(TestCase):

    fixtures = ['fixtures/organization.json','fixtures/country.json']

    def setUp(self):
        # dbSetup()
        self.indicators = factories.RandomIndicatorFactory.create_batch(2)
        self.tola_user = factories.TolaUser()

    def test_indicator_exists(self):
        """Check for Indicator object"""
        # indicator = Indicator.objects.get(name="Test Indicator One")
        # self.assertEqual(Indicator.objects.filter(id=indicator.id).count(), 1)
        for ind in self.indicators:
            print("%s - %s " % (ind.number, ind.name ))

        print(self.tola_user)
        self.assertEqual(Indicator.objects.count(), 2)

    def ztest_collected_exists(self):
        """Check for CollectedData object"""
        indicatorDataRecord = CollectedData.objects.get(description="somevaluecollected")
        self.assertEqual(CollectedData.objects.filter(id=indicatorDataRecord.id).count(), 1)
