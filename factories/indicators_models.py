from factory import DjangoModelFactory, post_generation, SubFactory, fuzzy

from indicators.models import (
    CollectedData as CollectedDataM,
    DisaggregationType as DisaggregationTypeM,
    DisaggregationLabel as DisaggregationLabelM,
    DisaggregationValue as DisaggregationValueM,
    ExternalService as ExternalServiceM,
    Frequency as FrequencyM,
    Indicator as IndicatorM,
    IndicatorType as IndicatorTypeM,
    Level as LevelM,
    Objective as ObjectiveM,
    PeriodicTarget as PeriodicTargetM,
    ReportingPeriod as ReportingPeriodM,
    StrategicObjective as StrategicObjectiveM,
    TolaTable as TolaTableM,
)
from .workflow_models import (Organization, WorkflowLevel1)


class DisaggregationType(DjangoModelFactory):
    class Meta:
        model = DisaggregationTypeM
        django_get_or_create = ('disaggregation_type',)

    disaggregation_type = 'Type Test'
    organization = SubFactory(Organization)


class DisaggregationLabel(DjangoModelFactory):
    class Meta:
        model = DisaggregationLabelM
        django_get_or_create = ('label',)

    label = 'Label Test'
    disaggregation_type = SubFactory(DisaggregationType)


class DisaggregationValue(DjangoModelFactory):
    class Meta:
        model = DisaggregationValueM

    disaggregation_label = SubFactory(DisaggregationLabel)


class Frequency(DjangoModelFactory):
    class Meta:
        model = FrequencyM

    frequency = 'Bi-weekly'
    description = 'Every two weeks'
    organization = SubFactory(Organization)


class Indicator(DjangoModelFactory):
    class Meta:
        model = IndicatorM

    name = 'Building resilience in Mali'

    @post_generation
    def workflowlevel1(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of workflowlevel1 were passed in, use them
            for workflowlevel1 in extracted:
                self.workflowlevel1.add(workflowlevel1)

    @post_generation
    def disaggregation(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of disaggregation were passed in, use them
            for disaggregation in extracted:
                self.disaggregation.add(disaggregation)


class Objective(DjangoModelFactory):
    class Meta:
        model = ObjectiveM

    name = 'Macht Deutschland wieder gesund'


class Level(DjangoModelFactory):
    class Meta:
        model = LevelM

    name = 'Intermediate Results'
    workflowlevel1 = SubFactory(WorkflowLevel1)


class CollectedData(DjangoModelFactory):
    class Meta:
        model = CollectedDataM

    workflowlevel1 = SubFactory(WorkflowLevel1)
    indicator = SubFactory(Indicator)


class IndicatorType(DjangoModelFactory):
    class Meta:
        model = IndicatorTypeM
        django_get_or_create = ('indicator_type',)

    indicator_type = fuzzy.FuzzyText()


class ExternalService(DjangoModelFactory):
    class Meta:
        model = ExternalServiceM

    name = 'External Service A'
    organization = SubFactory(Organization)


class ReportingPeriod(DjangoModelFactory):
    class Meta:
        model = ReportingPeriodM

    period = 'Quarter 1/2018'


class StrategicObjective(DjangoModelFactory):
    class Meta:
        model = StrategicObjectiveM

    name = 'Strategic Objective A'


class PeriodicTarget(DjangoModelFactory):
    class Meta:
        model = PeriodicTargetM


class TolaTable(DjangoModelFactory):
    class Meta:
        model = TolaTableM

    name = 'Table A'
    organization = SubFactory(Organization)

    @post_generation
    def country(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of country were passed in, use them
            for country in extracted:
                self.country.add(country)

    @post_generation
    def workflowlevel1(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of workflowlevel1 were passed in, use them
            for workflowlevel1 in extracted:
                self.workflowlevel1.add(workflowlevel1)
