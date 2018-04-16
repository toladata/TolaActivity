from django.template.defaultfilters import slugify
from factory import DjangoModelFactory, lazy_attribute, LazyAttribute, \
    SubFactory, post_generation, Sequence

import random

from workflow.models import (
    Contact as ContactM,
    Country as CountryM,
    Documentation as DocumentationM,
    FundCode as FundCodeM,
    Organization as OrganizationM,
    ProfileType as ProfileTypeM,
    ProjectType as ProjectTypeM,
    Sector as SectorM,
    SiteProfile as SiteProfileM,
    Stakeholder as StakeholderM,
    StakeholderType as StakeholderTypeM,
    TolaSites as TolaSitesM,
    TolaUser as TolaUserM,
    Program as ProgramM,
)
from .django_models import UserFactory, Group, Site


class CountryFactory(DjangoModelFactory):
    class Meta:
        model = CountryM
        django_get_or_create = ('code',)

    country = 'Afghanistan'
    code = 'AF'


class Contact(DjangoModelFactory):
    class Meta:
        model = ContactM

    name = 'Aryana Sayeed'
    city = 'Kabul'
    email = lazy_attribute(lambda o: slugify(o.name) + "@external-contact.com")
    phone = '+93 555444333'
    country = SubFactory(CountryFactory)


class OrganizationFactory(DjangoModelFactory):
    class Meta:
        model = OrganizationM

    name = 'MC Org'


class SiteProfileFactory(DjangoModelFactory):
    class Meta:
        model = SiteProfileM

    name = Sequence(lambda n: 'Site Profile {0}'.format(n))
    country = SubFactory(CountryFactory, country='United States', code='US')


class TolaUserFactory(DjangoModelFactory):
    class Meta:
        model = TolaUserM
        django_get_or_create = ('user',)

    user = SubFactory(UserFactory)
    name = LazyAttribute(lambda o: o.user.first_name + " " + o.user.last_name)
    organization = SubFactory(OrganizationFactory)
    country = SubFactory(CountryFactory, country='United States', code='US')


class ProgramFactory(DjangoModelFactory):
    class Meta:
        model = ProgramM

    name = 'Health and Survival for Syrians in Affected Regions'
    gaitid = Sequence(lambda n: "%0030d" % n)

    @post_generation
    def country(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if type(extracted) is list:
            # A list of country were passed in, use them
            for country in extracted:
                self.country.add(country)
        else:
            self.country.add(CountryFactory(country='Syria', code='SY'))


class Documentation(DjangoModelFactory):
    class Meta:
        model = DocumentationM

    name = 'Strengthening access and demand in Mandera County'
    program = SubFactory(ProgramFactory)


class SectorFactory(DjangoModelFactory):
    class Meta:
        model = SectorM

    sector = Sequence(lambda n: 'Sector {0}'.format(n))


class Stakeholder(DjangoModelFactory):
    class Meta:
        model = StakeholderM

    name = 'Stakeholder A'
    organization = SubFactory(OrganizationFactory)

    @post_generation
    def program(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if type(extracted) is list:
            # A list of program were passed in, use them
            for program in extracted:
                self.program.add(program)


class FundCode(DjangoModelFactory):
    class Meta:
        model = FundCodeM

    name = 'Fund Code A'
    organization = SubFactory(OrganizationFactory)


class ProjectType(DjangoModelFactory):
    class Meta:
        model = ProjectTypeM

    name = 'Adaptive Management'
    description = 'Adaptive Management'


class StakeholderType(DjangoModelFactory):
    class Meta:
        model = StakeholderTypeM

    name = 'Association'


class ProfileType(DjangoModelFactory):
    class Meta:
        model = ProfileTypeM

    profile = 'Distribution Center'


class TolaSites(DjangoModelFactory):
    class Meta:
        model = TolaSitesM
        django_get_or_create = ('name',)

    name = 'MercyCorps'
    site = SubFactory(Site)

