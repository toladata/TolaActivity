from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client

from indicators.models import Indicator, IndicatorType, DisaggregationType, Frequency, CollectedData, Level
from workflow.models import WorkflowLevel1, Country, Organization


class IndicatorTestCase(TestCase):
    fixtures = ['fixtures/001_organization.json', 'fixtures/config/sites.json']

    def setUp(self):
        new_organization = Organization.objects.create(name="tola")
        new_organization.save()
        get_organization = Organization.objects.get(name="tola")
        new_country = Country.objects.create(country="testcountry")
        new_country.save()
        get_country = Country.objects.get(country="testcountry")
        new_program = WorkflowLevel1.objects.create(name="testprogram")
        new_program.save()
        new_program.country.add(get_country)
        get_program = WorkflowLevel1.objects.get(name="testprogram")
        new_indicator_type = IndicatorType.objects.create(indicator_type="testtype")
        new_indicator_type.save()
        get_indicator_type = IndicatorType.objects.get(indicator_type="testtype")
        new_disaggregation = DisaggregationType.objects.create(organization=get_organization,
                                                               disaggregation_type="disagg")
        new_disaggregation.save()
        get_disaggregation = DisaggregationType.objects.get(disaggregation_type="disagg")
        new_frequency = Frequency.objects.create(frequency="newfreq")
        new_frequency.save()
        get_frequency = Frequency.objects.get(frequency="newfreq")
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        user.save()
        User.objects.get(username='john')
        new_indicator = Indicator.objects.create(name="testindicator", number="1.2.3", source="testing",
                                                 baseline="10", lop_target="10", reporting_frequency=get_frequency)
        new_indicator.save()
        new_indicator.disaggregation.add(get_disaggregation)
        new_indicator.indicator_type.add(get_indicator_type)
        new_indicator.workflowlevel1.add(get_program)

        get_indicator = Indicator.objects.get(name="testindicator")
        new_collected = CollectedData.objects.create(achieved="20", description="somevaluecollected",
                                                     indicator=get_indicator)
        new_collected.save()

    def test_indicator_exists(self):
        get_indicator = Indicator.objects.get(name="testindicator")
        self.assertEqual(Indicator.objects.filter(id=get_indicator.id).count(), 1)

    def test_collected_exists(self):
        get_collected = CollectedData.objects.get(description="somevaluecollected")
        self.assertEqual(CollectedData.objects.filter(id=get_collected.id).count(), 1)
