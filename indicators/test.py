from django.test import TestCase
from django.test import RequestFactory
from django.test import Client
from indicators.models import Indicator, IndicatorType, Objective, DisaggregationType, ReportingFrequency, CollectedData
from activitydb.models import Program, Sector
from django.contrib.auth.models import User


class IndicatorTestCase(TestCase):


    def setUp(self):
        new_program = Program.objects.create(name="testprogram")
        new_program.save()
        get_program = Program.objects.get(name="testprogram")
        new_indicator_type = IndicatorType.objects.create(indicator_type="testtype")
        new_indicator_type.save()
        get_indicator_type = IndicatorType.objects.get(indicator_type="testtype")
        new_disaggregation = DisaggregationType.objects.create(disaggregation_type="disagg")
        new_disaggregation.save()
        get_disaggregation = DisaggregationType.objects.get(disaggregation_type="disagg")
        new_frequency = ReportingFrequency.objects.create(frequency="newfreq")
        new_frequency.save()
        get_frequency = ReportingFrequency.objects.get(frequency="newfreq")
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        get_user = User.objects.get(username='john')
        new_indicator = Indicator.objects.create(name="testindicator",number="1.2.3",source="testing",
                                                 disaggregation=get_disaggregation, baseline="10",lop_target="10", reporting_frequency=get_frequency,owner=get_user)
        new_indicator.save()
        get_indicator = Indicator.objects.get(name="testindicator")
        new_collected = CollectedData.objects.create(targeted="12",achieved="20", description="somevaluecollected", indicator=get_indicator)
        new_collected.save()

    def test_indicator_exists(self):
        """Check for Indicator object"""
        get_indicator = Indicator.objects.get(name="testindicator")
        self.assertEqual(Indicator.objects.filter(id=get_indicator.id).count(), 1)

    def test_collected_exists(self):
        """Check for CollectedData object"""
        get_collected = CollectedData.objects.get(description="somevaluecollected")
        self.assertEqual(CollectedData.objects.filter(id=get_collected.id).count(), 1)

