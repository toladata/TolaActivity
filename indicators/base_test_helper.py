import datetime
from django.utils import timezone

from indicators.models import IndicatorType, Indicator,\
        PeriodicTarget, DisaggregationType, ReportingFrequency, CollectedData
from workflow.models import Program, Country, Organization
from django.contrib.auth.models import User

def populateDbWithTestData():
    mcOrg = Organization.objects.create(\
                name="Mercy Corps", level_1_label="Program", \
                level_2_label="Project", level_3_label="Component", \
                level_4_label="Activity", create_date=timezone.now())

    country = Country.objects.create(country="United States", organization=mcOrg)

    program = Program.objects.create(\
                gaitid=1000, name="TolaData Test", \
                funding_status="Funded", create_date=timezone.now())


    indicatorType = IndicatorType.objects.create(indicator_type="Output", create_date=timezone.now())

    disaggregationType = DisaggregationType.objects.create(disaggregation_type="SADD", create_date=timezone.now())


    reportingFrequency = ReportingFrequency.objects.create(frequency="newfreq")

    user = User.objects.create_user('joe', 'joe@example.org', 'joepassword')

    indicator = Indicator.objects.create(name="Test Indicator One", \
                    number="1.1.1", source="testing", baseline=10,\
                    lop_target="100", reporting_frequency=reportingFrequency)

    indicator.disaggregation.add(disaggregationType)
    indicator.indicator_type.add(indicatorType)
    indicator.program.add(program)
    indicator.save()

    dataRecord = CollectedData.objects.create(\
                    achieved=20, description="somevaluecollected",
                    indicator=indicator)
