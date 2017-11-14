from django.template.defaultfilters import slugify
from factory import DjangoModelFactory, lazy_attribute, LazyAttribute, \
    SubFactory, post_generation, PostGeneration

from workflow.models import (
    ApprovalType as ApprovalTypeM,
    Contact as ContactM,
    Country as CountryM,
    Documentation as DocumentationM,
    Organization as OrganizationM,
    Portfolio as PortfolioM,
    Sector as SectorM,
    SiteProfile as SiteProfileM,
    TolaUser as TolaUserM,
    WorkflowTeam as WorkflowTeamM,
    WorkflowLevel1 as WorkflowLevel1M,
    WorkflowLevel2 as WorkflowLevel2M,
)
from .user_models import User, Group


class ApprovalType(DjangoModelFactory):
    class Meta:
        model = ApprovalTypeM

    name = 'Approval Type A'


class Country(DjangoModelFactory):
    class Meta:
        model = CountryM

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

    name = 'Tola Org'


class SiteProfile(DjangoModelFactory):
    class Meta:
        model = SiteProfileM

    name = 'Tola Site'


class TolaUser(DjangoModelFactory):
    class Meta:
        model = TolaUserM

    user = SubFactory(User)
    name = LazyAttribute(lambda o: o.user.first_name + " " + o.user.last_name)
    organization = SubFactory(Organization)
    position_description = 'Chief of Operations'
    country = SubFactory(Country, country='Germany', code='DE')


class WorkflowLevel1(DjangoModelFactory):
    class Meta:
        model = WorkflowLevel1M

    name = 'Health and Survival for Syrians in Affected Regions'


class WorkflowTeam(DjangoModelFactory):
    class Meta:
        model = WorkflowTeamM

    workflow_user = SubFactory(TolaUser)
    workflowlevel1 = SubFactory(WorkflowLevel1)
    salary = '60,000'
    role = SubFactory(Group)


class WorkflowLevel2(DjangoModelFactory):
    class Meta:
        model = WorkflowLevel2M

    name = 'Help Syrians'
    total_estimated_budget = 15000
    actual_cost = 2900
    workflowlevel1 = SubFactory(WorkflowLevel1)


class Documentation(DjangoModelFactory):
    class Meta:
        model = DocumentationM

    name = 'Strengthening access and demand in Mandera County'
    workflowlevel1 = SubFactory(WorkflowLevel1)


class Sector(DjangoModelFactory):
    class Meta:
        model = SectorM

    sector = 'Basic Needs'


class Portfolio(DjangoModelFactory):
    class Meta:
        model = PortfolioM

    name = 'Syrian programs'
    description = 'Projects developed in Syria'
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
        else:
            self.country.add(Country(country='Syria', code='SY'))
