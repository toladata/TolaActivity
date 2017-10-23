from django.template.defaultfilters import slugify
from factory import DjangoModelFactory, lazy_attribute, LazyAttribute, SubFactory

from workflow.models import (
    Contact as ContactM,
    Country as CountryM,
    Organization as OrganizationM,
    TolaUser as TolaUserM,
)


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
    email = lazy_attribute(lambda o: o.name + "@external-contact.com")
    phone = '+93 555444333'
    country = SubFactory(Country)


class User(DjangoModelFactory):
    class Meta:
        model = 'auth.User'
        django_get_or_create = ('username',)

    first_name = 'Thom'
    last_name = 'Yorke'
    username = lazy_attribute(lambda o: slugify(o.first_name + '.' + o.last_name))
    email = lazy_attribute(lambda o: o.username + "@testenv.com")


class Organization(DjangoModelFactory):
    class Meta:
        model = OrganizationM

    name = 'Tola Org'


class TolaUser(DjangoModelFactory):
    class Meta:
        model = TolaUserM

    user = SubFactory(User)
    name = LazyAttribute(lambda o: o.user.first_name + " " + o.user.last_name)
    organization = SubFactory(Organization)
    position_description = 'Chief of Operations'
    country = SubFactory(Country, country='Germany', code='DE')
