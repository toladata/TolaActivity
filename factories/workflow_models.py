# -*- coding: utf-8 -*-
from django.template.defaultfilters import slugify
from factory import DjangoModelFactory, lazy_attribute, LazyAttribute, \
    SubFactory, post_generation

import random

from workflow.models import (
    ApprovalWorkflow as ApprovalWorkflowM,
    ApprovalType as ApprovalTypeM,
    Award as AwardM,
    Budget as BudgetM,
    Country as CountryM,
    Documentation as DocumentationM,
    FundCode as FundCodeM,
    Internationalization as InternationalizationM,
    IssueRegister as IssueRegisterM,
    Milestone as MilestoneM,
    Organization as OrganizationM,
    Portfolio as PortfolioM,
    ProfileType as ProfileTypeM,
    ProjectType as ProjectTypeM,
    Sector as SectorM,
    SiteProfile as SiteProfileM,
    Stakeholder as StakeholderM,
    StakeholderType as StakeholderTypeM,
    TolaSites as TolaSitesM,
    TolaUser as TolaUserM,
    WorkflowTeam as WorkflowTeamM,
    WorkflowLevel1 as WorkflowLevel1M,
    WorkflowLevel1Sector as WorkflowLevel1SectorM,
    WorkflowLevel2 as WorkflowLevel2M,
    WorkflowLevel2Sort as WorkflowLevel2SortM,
    Dashboard as DashboardM,
    Widget as WidgetM,
    Office as OfficeM,
)
from .django_models import User, Group, Site


class Award(DjangoModelFactory):
    class Meta:
        model = AwardM

    name = 'Award A'
    status = 'open'


class ApprovalType(DjangoModelFactory):
    class Meta:
        model = ApprovalTypeM

    name = 'Approval Type A'


class ApprovalWorkflow(DjangoModelFactory):
    class Meta:
        model = ApprovalWorkflowM

    approval_type = SubFactory(ApprovalType)


class Budget(DjangoModelFactory):
    class Meta:
        model = BudgetM

    contributor = 'John Lennon'


class Country(DjangoModelFactory):
    class Meta:
        model = CountryM
        django_get_or_create = ('code',)

    country = 'Afghanistan'
    code = 'AF'


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
        django_get_or_create = ('user',)

    user = SubFactory(User)
    name = LazyAttribute(lambda o: o.user.first_name + " " + o.user.last_name)
    organization = SubFactory(Organization)
    position_description = 'Chief of Operations'
    country = SubFactory(Country, country='Germany', code='DE')


class Dashboard(DjangoModelFactory):
    class Meta:
        model = DashboardM

    user = SubFactory(TolaUser)
    name = "My crazy Dashboard"

    @post_generation
    def share(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if type(extracted) is list:
            # A list of shared users were passed in, use them
            for shared_user in extracted:
                self.share.add(shared_user)


class Widget(DjangoModelFactory):
    class Meta:
        model = WidgetM
        django_get_or_create = ('dashboard',)

    dashboard = SubFactory(Dashboard)
    title = "My Crazy Widget"


class WorkflowLevel1(DjangoModelFactory):
    class Meta:
        model = WorkflowLevel1M

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


class WorkflowLevel1Sector(DjangoModelFactory):
    class Meta:
        model = WorkflowLevel1SectorM


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


class Stakeholder(DjangoModelFactory):
    class Meta:
        model = StakeholderM

    name = 'Stakeholder A'
    organization = SubFactory(Organization)

    @post_generation
    def workflowlevel1(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if type(extracted) is list:
            # A list of workflowlevel1 were passed in, use them
            for workflowlevel1 in extracted:
                self.workflowlevel1.add(workflowlevel1)


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

        if type(extracted) is list:
            # A list of country were passed in, use them
            for country in extracted:
                self.country.add(country)
        else:
            self.country.add(Country(country='Syria', code='SY'))


class Office(DjangoModelFactory):
    class Meta:
        model = OfficeM

    country = SubFactory(Country, country="Germany", code="DE")


class Internationalization(DjangoModelFactory):
    class Meta:
        model = InternationalizationM
        django_get_or_create = ('language',)

    language = 'de-DE'
    language_file = '{"name": "Name", "gender": "Geschlecht"}'


class IssueRegister(DjangoModelFactory):
    class Meta:
        model = IssueRegisterM

    name = 'IssueRegister A'


class Milestone(DjangoModelFactory):
    class Meta:
        model = MilestoneM

    name = 'Design Stage'


class TolaSites(DjangoModelFactory):
    class Meta:
        model = TolaSitesM
        django_get_or_create = ('name',)

    name = 'TolaData'
    site = SubFactory(Site)


class WorkflowLevel2Sort(DjangoModelFactory):
    class Meta:
        model = WorkflowLevel2SortM

    workflowlevel2_id = random.randint(1, 9999)

