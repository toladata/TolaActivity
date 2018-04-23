from factory import DjangoModelFactory, post_generation, SubFactory, fuzzy

from indicators.models import (
    CollectedData as CollectedDataM,
    DisaggregationType as DisaggregationTypeM,
    ExternalService as ExternalServiceM,
    Frequency as FrequencyM,
    Indicator as IndicatorM,
    IndicatorType as IndicatorTypeM,
    Level as LevelM,
    Objective as ObjectiveM,
    PeriodicTarget as PeriodicTargetM,
    StrategicObjective as StrategicObjectiveM,
)
from .workflow_models import (Organization, WorkflowLevel1)


class DisaggregationType(DjangoModelFactory):
    class Meta:
        model = DisaggregationTypeM
        django_get_or_create = ('disaggregation_type',)

    organization = SubFactory(Organization)


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


class StrategicObjective(DjangoModelFactory):
    class Meta:
        model = StrategicObjectiveM

    name = 'Strategic Objective A'


class PeriodicTarget(DjangoModelFactory):
    class Meta:
        model = PeriodicTargetM
