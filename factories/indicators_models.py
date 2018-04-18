from random import randint

import faker
from django.utils import timezone
from factory import DjangoModelFactory, post_generation, SubFactory, fuzzy, \
    lazy_attribute, Sequence, RelatedFactory

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
from workflow_models import OrganizationFactory, ProgramFactory

FAKER = faker.Faker(locale='en_US')


class ReportingFrequency(DjangoModelFactory):
    class Meta:
        model = ReportingFrequencyM

    frequency = 'Bi-weekly'
    description = 'Every two weeks'
    organization = SubFactory(OrganizationFactory)


class RandomIndicatorFactory(DjangoModelFactory):
    class Meta:
        model = IndicatorM

    name = lazy_attribute(lambda n: FAKER.sentence(nb_words=8))
    number = lazy_attribute(
        lambda n: "%s.%s.%s" % (randint(1, 2), randint(1, 4), randint(1, 5)))
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

    name = Sequence(lambda n: 'Indicator {0}'.format(n))
    program = RelatedFactory(ProgramFactory, name=Sequence(lambda n: 'Program {0}'.format(n)))


class Objective(DjangoModelFactory):
    class Meta:
        model = ObjectiveM

    name = 'Get Tola rocking!'


class LevelFactory(DjangoModelFactory):
    class Meta:
        model = LevelM

    name = Sequence(lambda n: 'Level: {0}'.format(n))


class CollectedDataFactory(DjangoModelFactory):
    class Meta:
        model = CollectedDataM

    program = SubFactory(ProgramFactory)
    indicator = SubFactory(IndicatorFactory)
    achieved = 10


class IndicatorTypeFactory(DjangoModelFactory):
    class Meta:
        model = IndicatorTypeM
        django_get_or_create = ('indicator_type',)

    indicator_type = Sequence(lambda n: 'Indicator Type {0}'.format(n))


class ExternalServiceFactory(DjangoModelFactory):
    class Meta:
        model = ExternalServiceM

    name = Sequence(lambda n: 'External Service {0}'.format(n))


class StrategicObjective(DjangoModelFactory):
    class Meta:
        model = StrategicObjectiveM

    name = Sequence(lambda n: 'Stratigic Objective {0}'.format(n))


class PeriodicTarget(DjangoModelFactory):
    class Meta:
        model = PeriodicTargetM
