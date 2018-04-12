import factory
import faker
from random import randint
from django.utils import timezone

from factory import DjangoModelFactory, create, post_generation, SubFactory, fuzzy, lazy_attribute

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

FAKER = faker.Faker(locale='en_US')


class ReportingFrequency(DjangoModelFactory):
    class Meta:
        model = ReportingFrequencyM

    frequency = 'Bi-weekly'
    description = 'Every two weeks'
    organization = SubFactory(Organization)


class RandomIndicatorFactory(DjangoModelFactory):

    class Meta:
        model = IndicatorM

    name = lazy_attribute(lambda n: FAKER.sentence(nb_words=8))
    number = lazy_attribute(lambda n: "%s.%s.%s" % (randint(1,2), randint(1,4), randint(1,5)))
    create_date = lazy_attribute(lambda t: timezone.now())

    @post_generation
    def program(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if type(extracted) is list:
            # A list of program were passed in, use them
            for program in extracted:
                self.program.add(program)
        elif extracted:
            self.program.add(extracted)
        else:
            pass


class IndicatorFactory(DjangoModelFactory):
    class Meta:
        model = IndicatorM

    name = 'Building resilience in Mali'

    @post_generation
    def program(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if type(extracted) is not list:
            extracted = [extracted]

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
    indicator = SubFactory(IndicatorFactory)


class IndicatorTypeFactory(DjangoModelFactory):
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