from django.template.defaultfilters import slugify
from factory import DjangoModelFactory, lazy_attribute, LazyAttribute, \
    SubFactory, post_generation

from workflow.models import (
    Contact as ContactM,
    Country as CountryM,
    Organization as OrganizationM,
    SiteProfile as SiteProfileM,
    TolaUser as TolaUserM,
    WorkflowTeam as WorkflowTeamM,
    WorkflowLevel1 as WorkflowLevel1M,
    WorkflowLevel2 as WorkflowLevel2M,
)
from .user_models import User


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


class WorkflowTeam(DjangoModelFactory):
    class Meta:
        model = WorkflowTeamM


class WorkflowLevel1(DjangoModelFactory):
    class Meta:
        model = WorkflowLevel1M

    name = 'Health and Survival for Syrians in Affected Regions'


class WorkflowLevel2(DjangoModelFactory):
    class Meta:
        model = WorkflowLevel2M

    name = 'Help Syrians'

    @post_generation
    def site(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of site were passed in, use them
            for site in extracted:
                self.site.add(site)
