from django.template.defaultfilters import slugify
from factory import DjangoModelFactory, lazy_attribute, LazyAttribute, \
    SubFactory, post_generation

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


class Country(DjangoModelFactory):
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
    country = SubFactory(Country)


class Organization(DjangoModelFactory):
    class Meta:
        model = OrganizationM

    name = 'MC Org'


class SiteProfile(DjangoModelFactory):
    class Meta:
        model = SiteProfileM

    name = 'MC Site'


class TolaUser(DjangoModelFactory):
    class Meta:
        model = TolaUserM
        django_get_or_create = ('user',)

    user = SubFactory(UserFactory)
    name = LazyAttribute(lambda o: o.user.first_name + " " + o.user.last_name)
    organization = SubFactory(Organization)
    country = SubFactory(Country, country='United States', code='US')




class Program(DjangoModelFactory):
    class Meta:
        model = ProgramM

    name = 'Health and Survival for Syrians in Affected Regions'

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
            self.country.add(Country(country='Syria', code='SY'))


class Documentation(DjangoModelFactory):
    class Meta:
        model = DocumentationM

    name = 'Strengthening access and demand in Mandera County'
    program = SubFactory(Program)


class Sector(DjangoModelFactory):
    class Meta:
        model = SectorM

    sector = 'Basic Needs'


class Stakeholder(DjangoModelFactory):
    class Meta:
        model = StakeholderM

    name = 'Stakeholder A'
    organization = SubFactory(Organization)

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
    organization = SubFactory(Organization)


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

