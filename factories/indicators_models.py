import factory
import faker
from factory import DjangoModelFactory, post_generation, SubFactory, fuzzy, lazy_attribute

from indicators.models import (
    CollectedData as CollectedDataM,
    ExternalService as ExternalServiceM,
    ReportingFrequency as ReportingFrequencyM,
    Indicator as IndicatorM,
    IndicatorType as IndicatorTypeM,
    Level as LevelM,
    Objective as ObjectiveM,
    PeriodicTarget as PeriodicTargetM,
    StrategicObjective as StrategicObjectiveM,
)
from workflow.models import Organization, Program

class ReportingFrequency(DjangoModelFactory):
    class Meta:
        model = ReportingFrequencyM

    frequency = 'Bi-weekly'
    description = 'Every two weeks'
    organization = SubFactory(Organization)


fake = faker.Faker()
class RandomIndicatorFactory(DjangoModelFactory):

    class Meta:
        model = IndicatorM

    name = factory.Faker('sentence', nb_words=8)

    @lazy_attribute
    def number(self):

        return "%s.%s.%s" % (str(fake.pyint())[:1], str(fake.pyint())[:1], str(fake.pyint())[:1])

    @post_generation
    def program(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of program were passed in, use them
            for program in extracted:
                self.program.add(program)

class Indicator(DjangoModelFactory):
    class Meta:
        model = IndicatorM

    name = 'Building resilience in Mali'

    @post_generation
    def program(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of program were passed in, use them
            for program in extracted:
                self.program.add(program)


class Objective(DjangoModelFactory):
    class Meta:
        model = ObjectiveM

    name = 'Get Tola rocking!'


class Level(DjangoModelFactory):
    class Meta:
        model = LevelM

    name = 'Output'
    program = SubFactory(Program)


class CollectedData(DjangoModelFactory):
    class Meta:
        model = CollectedDataM

    program = SubFactory(Program)
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