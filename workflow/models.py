from __future__ import unicode_literals
from decimal import Decimal
import uuid

from django.db import models
from django.conf import settings
from django.contrib.postgres import fields
from django.contrib.auth.models import User, Group
from django.contrib.postgres.fields import HStoreField, JSONField, ArrayField
from django.contrib.sites.models import Site
from django.core.exceptions import ValidationError
from django.db.models import Q
try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone
from simple_history.models import HistoricalRecords
from voluptuous import Schema, All, Any, Length, Required

from search.utils import ElasticsearchIndexer

ROLE_SUPER_USER = 'SuperUser'
ROLE_ORGANIZATION_ADMIN = 'OrgAdmin'
ROLE_PROGRAM_ADMIN = 'ProgramAdmin'
ROLE_PROGRAM_TEAM = 'ProgramTeam'
ROLE_VIEW_ONLY = 'ViewOnly'
DEFAULT_PROGRAM_NAME = 'Default program'


class TolaSites(models.Model):
    name = models.CharField(blank=True, null=True, max_length=255)
    agency_name = models.CharField(blank=True, null=True, max_length=255)
    agency_url = models.CharField(blank=True, null=True, max_length=255)
    tola_report_url = models.CharField(default="https://report.toladata.io", null=True, max_length=255)
    tola_tables_url = models.CharField(default="https://activity.toladata.io", null=True, max_length=255)
    front_end_url = models.CharField(default="https://activity.toladata.io", null=True, max_length=255)
    tola_tables_user = models.CharField(blank=True, null=True, max_length=255)
    tola_tables_token = models.CharField(blank=True, null=True, max_length=255)
    site = models.ForeignKey(Site)
    privacy_disclaimer = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now=False, blank=True, null=True)
    updated = models.DateTimeField(auto_now=False, blank=True, null=True)
    whitelisted_domains = models.TextField("Whitelisted Domains", null=True, blank=True)

    class Meta:
        verbose_name = "Tola Site"
        verbose_name_plural = "Tola Sites"

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if kwargs.pop('new_entry', True):
            self.created = timezone.now()
        else:
            self.updated = timezone.now()
        return super(TolaSites, self).save(*args, **kwargs)
        

class Sector(models.Model):
    sector = models.CharField("Sector Name", max_length=255, blank=True)
    default_global = models.BooleanField(default=0)
    sector_nearest = models.ManyToManyField('self', symmetrical=False, through='SectorRelated', related_name="nearest")
    organization = models.ForeignKey("Organization", default=1, related_name="org_specific_sector")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='sectors', null=True, blank=True)

    class Meta:
        ordering = ('sector',)

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Sector, self).save()

    def __unicode__(self):
        return self.sector


class SectorRelated(models.Model):
    sector = models.ForeignKey(Sector)
    sector_related = models.ForeignKey(Sector, related_name='sector_related')
    organization = models.ForeignKey("Organization", default=1)
    order = models.PositiveIntegerField(default=0)
    org_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('order',)


class Currency(models.Model):
    source_currency = models.CharField("Source Currency Name", max_length=255, blank=True)
    target_currency = models.CharField("Target Currency Name", max_length=255, blank=True)
    current_rate = models.IntegerField("Conversion Rate", null=True, blank=True)
    conversion_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('source_currency',)
        verbose_name_plural = "Currencies"

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Currency, self).save()

    def __unicode__(self):
        return self.source_currency


class Organization(models.Model):
    organization_uuid = models.CharField(max_length=255, verbose_name='Organization UUID', default=uuid.uuid4, unique=True)
    name = models.CharField("Organization Name", max_length=255, blank=True, default="TolaData")
    description = models.TextField("Description/Notes", max_length=765, null=True, blank=True)
    organization_url = models.CharField(blank=True, null=True, max_length=255)
    sector = models.ManyToManyField(Sector, blank=True, related_name="org_sector")
    level_1_label = models.CharField("Project/Program Organization Level 1 label", default="Program", max_length=255, blank=True)
    level_2_label = models.CharField("Project/Program Organization Level 2 label", default="Project", max_length=255, blank=True)
    level_3_label = models.CharField("Project/Program Organization Level 3 label", default="Component", max_length=255, blank=True)
    level_4_label = models.CharField("Project/Program Organization Level 4 label", default="Activity", max_length=255, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    chargebee_subscription_id = models.CharField(blank=True, null=True, max_length=50)
    chargebee_used_seats = models.IntegerField(blank=True, null=True, default=0)
    oauth_domains = fields.ArrayField(models.CharField("OAuth Domains", max_length=255, null=True, blank=True), null=True, blank=True)
    date_format = models.CharField("Date Format", max_length=50, blank=True, default="DD.MM.YYYY")
    default_currency = models.ForeignKey(Currency, blank=True, null=True)
    currency_format = models.CharField("Currency Format", max_length=50, blank=True, default="Commas")
    allow_budget_decimal = models.BooleanField("Allow Budget in Decimal", default=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Organizations"
        app_label = 'workflow'

    def clean_fields(self, exclude=None):
        super(Organization, self).clean_fields(exclude=exclude)
        if self.oauth_domains:
            if Organization.objects.filter(
                    oauth_domains__overlap=self.oauth_domains
            ).exclude(organization_uuid=self.organization_uuid).exists():
                raise ValidationError(
                    'Oauth Domain already used by another organization')

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Organization, self).save()

    def __unicode__(self):
        return self.name


class Country(models.Model):
    country = models.CharField("Country Name", max_length=255, blank=True)
    code = models.CharField("2 Letter Country Code", max_length=4, blank=True)
    description = models.TextField("Description/Notes", max_length=765,blank=True)
    latitude = models.CharField("Latitude", max_length=255, null=True, blank=True)
    longitude = models.CharField("Longitude", max_length=255, null=True, blank=True)
    zoom = models.IntegerField("Zoom", default=5)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('country',)
        verbose_name_plural = "Countries"
        app_label = 'workflow'

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Country, self).save()

    def __unicode__(self):
        return self.country


TITLE_CHOICES = (
    ('mr', 'Mr.'),
    ('mrs', 'Mrs.'),
    ('ms', 'Ms.'),
)


class TolaUser(models.Model):
    """
    TolaUser is the registered user who belongs to some organization and can manage its projects.
    """
    tola_user_uuid = models.CharField(max_length=255, verbose_name='TolaUser UUID', default=uuid.uuid4, unique=True)
    title = models.CharField(blank=True, null=True, max_length=3, choices=TITLE_CHOICES)
    name = models.CharField("Given Name", blank=True, null=True, max_length=100)
    employee_number = models.IntegerField("Employee Number", blank=True, null=True)
    position_description = models.CharField(blank=True, null=True, max_length=255)
    contact_info = models.CharField(blank=True, null=True, max_length=255)
    user = models.OneToOneField(User, unique=True, related_name='tola_user')
    organization = models.ForeignKey(Organization, default=1, blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True)
    countries = models.ManyToManyField(Country, verbose_name="Accessible Countries", related_name='countries',
                                       blank=True)
    tables_api_token = models.CharField(blank=True, null=True, max_length=255)      # Todo delete maybe?
    activity_api_token = models.CharField(blank=True, null=True, max_length=255)    # Todo delete maybe?
    privacy_disclaimer_accepted = models.BooleanField(default=False)
    filter = JSONField(blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        if (settings.TOLAUSER_OBFUSCATED_NAME and
                    self.name == settings.TOLAUSER_OBFUSCATED_NAME):
            if self.user.first_name and self.user.last_name:
                return u'{} {}'.format(self.user.first_name,
                                       self.user.last_name)
            else:
                return u'-'
        else:
            return self.name if self.name else u'-'

    @property
    def countries_list(self):
        return ', '.join([x.code for x in self.countries.all()])

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()

        if settings.TOLAUSER_OBFUSCATED_NAME:
            self.name = settings.TOLAUSER_OBFUSCATED_NAME

        super(TolaUser, self).save()


class Award(models.Model):
    donors = models.ManyToManyField("Stakeholder", blank=True)
    name = models.CharField("Award Name/Title", blank=True, null=True, max_length=100)
    organization = models.ForeignKey(Organization, default=1)
    countries = models.ManyToManyField(Country, verbose_name="Countries", related_name='countries_award', blank=True)
    amount = models.IntegerField("Amount", blank=True, default=0)
    currency = models.ForeignKey(Currency,blank=True, null=True)
    award_currency = models.ForeignKey(Currency, blank=True, null=True, related_name="award_currency")

    STATUS_OPEN = "open"
    STATUS_FUNDED = "funded"
    STATUS_AWAITING = "awaiting"
    STATUS_CLOSED = "closed"
    AWARD_STATUS_CHOICES = (
        (STATUS_OPEN,"Open"),
        (STATUS_FUNDED,"Funded"),
        (STATUS_AWAITING, "Awaiting Funding"),
        (STATUS_CLOSED,"Closed")
    )

    status = models.CharField(choices=AWARD_STATUS_CHOICES, max_length=50, default="Open")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    @property
    def countries_list(self):
        return ', '.join([x.code for x in self.countries.all()])

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Award, self).save()


class Internationalization(models.Model):
    language = models.CharField("Language", blank=True, null=True, max_length=100)
    language_file = JSONField()
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('language',)

    def __unicode__(self):
        return self.language

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Internationalization, self).save()


class TolaBookmarks(models.Model):
    user = models.ForeignKey(TolaUser, related_name='tolabookmark')
    name = models.CharField(blank=True, null=True, max_length=255)
    bookmark_url = models.CharField(blank=True, null=True, max_length=255)
    filter = models.CharField(blank=True, null=True, max_length=255)
    workflowlevel1 = models.ForeignKey("WorkflowLevel1", blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Tola Bookmarks"

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(TolaBookmarks, self).save()

"""
dashboard = { user_id: string (link to tola user endpoint) name: string (name of the dashboard)
(required widgets: Array of widgets (link to widget endpoint) share: Array of tola user url (link to tola user endpoint) }


widget = { w: number, h: number, x: number, y: number, xSm: number, ySm: number, 
xMd: number, yMd: number, xLg: number, yLg: number, xXl: number, yXl: number, dragAndDrop: boolean, resizable: boolean, title: string (required), type: string (required), data: JSON Object }

"""


class Widget(models.Model):
    w = models.IntegerField(default=0, null=True, blank=True)
    h = models.IntegerField(default=0, null=True, blank=True)
    x = models.IntegerField(default=0, null=True, blank=True)
    y = models.IntegerField(default=0, null=True, blank=True)
    xSm = models.IntegerField(default=0, null=True, blank=True)
    ySm = models.IntegerField(default=0, null=True, blank=True)
    xMd = models.IntegerField(default=0, null=True, blank=True)
    yMd = models.IntegerField(default=0, null=True, blank=True)
    xLg = models.IntegerField(default=0, null=True, blank=True)
    yLg = models.IntegerField(default=0, null=True, blank=True)
    xXl = models.IntegerField(default=0, null=True, blank=True)
    yXl = models.IntegerField(default=0, null=True, blank=True)
    drag_and_drop = models.BooleanField(default=0)
    resizable = models.BooleanField(default=0)
    changed = models.BooleanField(default=0)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    data = JSONField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('title',)
        verbose_name_plural = "Widgets"

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Widget, self).save()


class Dashboard(models.Model):
    dashboard_uuid = models.UUIDField(editable=False, verbose_name='Dashboard UUID', default=uuid.uuid4, unique=True)
    user = models.ForeignKey(TolaUser, related_name='toladashboard')
    # naming this with suffix _uuid interfears with public token generation
    created_by = models.CharField(max_length=255, verbose_name='TolaUser UUID', null=True, blank=True)
    name = models.CharField(blank=True, null=True, max_length=255)
    widgets = models.ManyToManyField(Widget, blank=True)
    share = models.ManyToManyField(TolaUser, blank=True)
    public = JSONField(blank=True, null=True, help_text="Public information with the structure:{all: (bool), org: (bool), url: (bool)}")
    public_url_token = models.CharField(max_length=255, blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    blacklist = ArrayField(models.CharField(max_length=255), blank=True, default=[])
    shared_wfl1_uuids = ArrayField(models.CharField(max_length=255), blank=True, default=[])

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Dashboards"

    def __unicode__(self):
        return self.name

    def _validate_public(self, public):
        schema = Schema({
            Required('all'): bool,
            Required('org'): bool,
            Required('url'): bool
        })
        return schema(public)

    def clean_fields(self, exclude=None):
        super(Dashboard, self).clean_fields(exclude=exclude)
        if self.public is not None:
            try:
                self.public = self._validate_public(self.public)
            except Exception as e:
                raise ValidationError(e)

    def save(self, *args, **kwargs):
        self.full_clean()
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Dashboard, self).save()


class TolaUserFilter(models.Model):
    user = models.ForeignKey(TolaUser, related_name="filter_user")
    country_filter = models.ManyToManyField(Country, blank=True, related_name="filter_country")
    workflowlevel1_filter = models.ManyToManyField("WorkflowLevel1", blank=True, related_name="filter_level1")
    workflowlevel2_filter = models.ManyToManyField("WorkflowLevel2", blank=True, related_name="filter_level2")
    sector_filter = models.ManyToManyField("Sector", blank=True, related_name="filter_sector")
    start_date_filter = models.DateField(blank=True, null=True)
    end_date_filter = models.DateField(blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('user',)

    def __unicode__(self):
        return self.user

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(TolaUserFilter, self).save()


class TolaUserProxy(TolaUser):

    class Meta:
        verbose_name, verbose_name_plural = u"Report Tola User", u"Report Tola Users"
        proxy = True


class ProjectType(models.Model):
    name = models.CharField("Type of Activity", max_length=135)
    description = models.CharField(max_length=765)
    default_global = models.BooleanField(default=0)
    organization = models.ForeignKey(Organization, default=1)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(ProjectType, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class FundCode(models.Model):
    name = models.CharField("Fund Code", max_length=255, blank=True)
    default_global = models.BooleanField(default=0)
    organization = models.ForeignKey(Organization, default=1)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(FundCode, self).save()

    def __unicode__(self):
        return self.name


class ApprovalType(models.Model):
    name = models.CharField("Name", max_length=255, blank=True)
    default_global = models.BooleanField(default=0)
    organization = models.ForeignKey(Organization, default=1)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name','organization')

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(ApprovalType, self).save()

    def __unicode__(self):
        return self.name


class ApprovalWorkflow(models.Model):
    note = models.TextField(null=True, blank=True)
    approval_type = models.ForeignKey(ApprovalType, null=True, related_name="approval_type", on_delete=models.SET_NULL)
    assigned_to = models.ForeignKey(TolaUser, null=False, related_name="to_approval")
    requested_from = models.ForeignKey(TolaUser, null=False, related_name="from_approval")
    date_assigned = models.DateTimeField(null=True, blank=True)
    date_approved = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='approval', null=True, blank=True)

    STATUS_OPEN = "open"
    STATUS_AWAITING_APPROVAL = "awaiting_approval"
    STATUS_TRACKING = "tracking"
    STATUS_AWAITING_VERIFICATION = "awaiting_verification"
    STATUS_CLOSED = "closed"

    STATUS_CHOICES = (
        (STATUS_OPEN, "Open"),
        (STATUS_AWAITING_APPROVAL, "Awaiting Approval"),
        (STATUS_TRACKING, "Tracking"),
        (STATUS_AWAITING_VERIFICATION, "Awaiting Verification"),
        (STATUS_CLOSED, "Closed")
    )

    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default="open")

    SECTIONS = (
        ('workflowlevel1', 'Workflow Level 1'),
        ('workflowlevel2', 'Workflow Level 2'),
        ('workflowlevel3', 'Workflow Level 3'),
        ('sites', 'Sites'),
        ('stakeholders', 'Stakeholders'),
        ('documents', 'Documents'),
    )

    section = models.CharField(choices=SECTIONS, max_length=50, default="workflowlevel1")

    class Meta:
        ordering = ('approval_type',)

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(ApprovalWorkflow, self).save()

    def __unicode__(self):
        return unicode(self.approval_type)


class Portfolio(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    organization = models.ForeignKey(Organization, blank=True, null=True)
    country = models.ManyToManyField(Country, blank=True)
    is_global = models.BooleanField(default=0)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Portfolio, self).save()

    def __unicode__(self):
        return unicode(self.name)


class Milestone(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    organization = models.ForeignKey(Organization, blank=True, null=True)
    milestone_start_date = models.DateTimeField(null=True, blank=True)
    milestone_end_date = models.DateTimeField(null=True, blank=True)
    is_global = models.BooleanField(default=0)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='milestones', null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Milestone, self).save()

    def __unicode__(self):
        return unicode(self.name)


class WorkflowLevel1(models.Model):
    level1_uuid = models.CharField(max_length=255, editable=False, verbose_name='WorkflowLevel1 UUID', default=uuid.uuid4, unique=True)
    unique_id = models.CharField("ID", max_length=255, blank=True, null=True, help_text="User facing unique ID field if needed")
    name = models.CharField("Name", max_length=255, blank=True)
    funding_status = models.CharField("Funding Status", max_length=255, blank=True, help_text='Funds have been approved to start working')
    cost_center = models.CharField("Fund Code", max_length=255, blank=True, null=True, help_text='Coded field for financial system integrations')
    fund_code = models.ManyToManyField(FundCode, blank=True, help_text='Coded field for financial system integrations')
    organization = models.ForeignKey(Organization, blank=True, null=True, help_text='Related Org to associate with')
    portfolio = models.ForeignKey(Portfolio, blank=True, null=True, help_text='Combine with a set or other level 1s for folder like structure')
    award = models.ManyToManyField(Award, blank=True, help_text='Funding source if used')
    description = models.TextField("Description", max_length=765, null=True, blank=True)
    sector = models.ManyToManyField(Sector, blank=True, help_text='Primary work type classification')
    sub_sector = models.ManyToManyField(Sector, blank=True, related_name="sub_sector", help_text='Additional work type classifications')
    country = models.ManyToManyField(Country, blank=True, help_text='Country location for work')
    milestone = models.ManyToManyField(Milestone, blank=True, help_text='Set of milestones or stated goals and dates for work')
    user_access = models.ManyToManyField(TolaUser, blank=True)
    public_dashboard = models.BooleanField("Enable Public Dashboard", default=False, help_text='Allow dashboards to be set to public if needed')
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    sort = models.IntegerField(default=0)  #sort array

    class Meta:
        ordering = ('name',)
        verbose_name = "Workflow Level 1"
        verbose_name_plural = "Workflow Level 1"

    def save(self, *args, **kwargs):
        if not 'force_insert' in kwargs:
            kwargs['force_insert'] = False
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()

        super(WorkflowLevel1, self).save()

        ei = ElasticsearchIndexer()
        ei.index_workflowlevel1(self)

    def delete(self, *args, **kwargs):
        super(WorkflowLevel1, self).delete(*args, **kwargs)

        ei = ElasticsearchIndexer()
        ei.delete_workflowlevel1(self)

    @property
    def countries(self):
        return ', '.join([x.country for x in self.country.all()])

    def __unicode__(self):
        if self.organization:
            return u"{} <{}>".format(self.name, self.organization.name)
        else:
            return self.name


class WorkflowLevel1Sector(models.Model):
    workflowlevel1 = models.ForeignKey(WorkflowLevel1, blank=True, null=True, related_name="level1_sectors")
    sector = models.ForeignKey(Sector, blank=True, null=True, related_name="level1_primary_sector")
    sub_sector = models.ManyToManyField(Sector, blank=True, related_name="level1_sub_sector")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    sort = models.IntegerField(default=0)  #sort array

    class Meta:
        ordering = ('create_date',)
        verbose_name = "Workflow Level 1 Sector"
        verbose_name_plural = "Workflow Level 1 Sectors"

    def save(self, *args, **kwargs):
        if not 'force_insert' in kwargs:
            kwargs['force_insert'] = False
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(WorkflowLevel1Sector, self).save()

    @property
    def sub_sectors(self):
        return ', '.join([x.sub_sector for x in self.sub_sector.all()])

    def __unicode__(self):
        return self.workflowlevel1.name


class WorkflowTeam(models.Model):
    workflow_user = models.ForeignKey(
        TolaUser, help_text='User', blank=True, null=True, related_name="auth_approving")
    workflowlevel1 = models.ForeignKey(WorkflowLevel1, null=True, blank=True)
    salary = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    role = models.ForeignKey(Group, null=True, blank=True)
    budget_limit = models.IntegerField(null=True, blank=True)
    country = models.ForeignKey("Country", null=True, blank=True)
    partner_org = models.ForeignKey(Organization, null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('workflow_user',)
        verbose_name = "Workflow Team"
        verbose_name_plural = "Workflow Teams"

    def clean(self):
        if self.role and self.role.name == ROLE_ORGANIZATION_ADMIN:
            raise ValidationError(
                'Workflowteam role can not be ROLE_ORGANIZATION_ADMIN'
            )

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(WorkflowTeam, self).save()

    def __unicode__(self):
        return u"{} - {} <{}>".format(self.workflow_user, self.role,
                                      self.workflowlevel1)


class Office(models.Model):
    name = models.CharField("Office Name", max_length=255, blank=True)
    code = models.CharField("Office Code", max_length=255, blank=True)
    organization = models.ForeignKey(Organization, blank=True, null=True, help_text='Related Org to associate with')
    country = models.ForeignKey(Country, verbose_name="Country")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Office, self).save()

    def __unicode__(self):
        if not self.code:
            return unicode(self.name)
        else:
            return u"{} - {}".format(self.name, self.code)


class ProfileType(models.Model):
    profile = models.CharField("Profile Type", max_length=255, blank=True)
    default_global = models.BooleanField(default=0)
    organization = models.ForeignKey(Organization, default=1)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('profile',)

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(ProfileType, self).save()

    def __unicode__(self):
        return self.profile


class LandType(models.Model):
    classify_land = models.CharField("Land Classification", help_text="Rural, Urban, Peri-Urban", max_length=100, blank=True)
    default_global = models.BooleanField(default=0)
    organization = models.ForeignKey(Organization, default=1)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('classify_land',)

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(LandType, self).save()

    def __unicode__(self):
        return self.classify_land


class SiteProfileManager(models.Manager):
    def get_queryset(self):
        return super(SiteProfileManager, self).get_queryset().prefetch_related().select_related('country', 'type')


class SiteProfile(models.Model):

    site_uuid = models.CharField(max_length=255, verbose_name='Site UUID', default=uuid.uuid4, unique=True)
    name = models.CharField("Site Name", max_length=255, blank=False)
    type = models.ForeignKey(ProfileType, blank=True, null=True, on_delete=models.SET_NULL)
    office = models.ForeignKey(Office, blank=True, null=True)
    contact_leader = models.CharField("Contact Name", max_length=255, blank=True, null=True)
    contact_number = models.CharField("Contact Number", max_length=255, blank=True, null=True)
    status = models.BooleanField("Site Active", default=True)
    address_line1 = models.CharField(max_length=255, null=True, blank=True)
    address_line2 = models.CharField(max_length=255, null=True, blank=True)
    address_line3 = models.CharField(max_length=255, null=True, blank=True)
    address_line4 = models.CharField(max_length=255, null=True, blank=True)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    country = models.ForeignKey(Country)
    city = models.CharField(max_length=85, null=True, blank=True)
    latitude = models.DecimalField("Latitude (Decimal Coordinates)", decimal_places=16,max_digits=25, default=Decimal("0.00"))
    longitude = models.DecimalField("Longitude (Decimal Coordinates)", decimal_places=16,max_digits=25, default=Decimal("0.00"))
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True, blank=True)
    workflowlevel1 = models.ManyToManyField(WorkflowLevel1, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='sites', null=True, blank=True)
    history = HistoricalRecords()
    notes = models.TextField(blank=True)
    #optimize query
    objects = SiteProfileManager()

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Site Profiles"

    def save(self, *args, **kwargs):

        # Check if a create date has been specified. If not, display today's date in create_date and edit_date
        if self.create_date == None:
            self.create_date = timezone.now()
            self.edit_date = timezone.now()

        super(SiteProfile, self).save()

    def __unicode__(self):
        new_name = self.name
        return new_name


class StakeholderType(models.Model):
    name = models.CharField("Stakeholder Type", max_length=255, blank=True, null=True)
    default_global = models.BooleanField(default=0)
    organization = models.ForeignKey(Organization, default=1)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Stakeholder Types"

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(StakeholderType, self).save()

    def __unicode__(self):
        return self.name


class StakeholderManager(models.Manager):
    def get_queryset(self):
        return super(StakeholderManager, self).get_queryset().prefetch_related('sectors').select_related(
            'country', 'type', 'formal_relationship_document', 'vetting_document')


class Stakeholder(models.Model):
    """
    A Stakeholder is an individual, group, or organization, who may affect, be affected by, or perceive itself to be
    affected by a decision, activity, or outcome of a project. This may be inside or outside an organization.

    Any or all of these premises can be met for a stakeholder:

    * Sponsors a project (with money or workforce).
    * Has an interest or a gain upon a successful completion of a project.
    * May have a positive or negative influence in the project completion.
    """
    stakeholder_uuid = models.CharField(max_length=255, verbose_name='Stakeholder UUID', default=uuid.uuid4, unique=True)
    name = models.CharField("Stakeholder/Organization Name", max_length=255, blank=True, null=True)
    type = models.ForeignKey(StakeholderType, blank=True, null=True)
    role = models.CharField("Role", max_length=255, blank=True, null=True)
    contribution = models.CharField("Contribution", max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True)
    organization = models.ForeignKey(Organization, default=1)
    workflowlevel1 = models.ManyToManyField(WorkflowLevel1, blank=True)
    sectors = models.ManyToManyField(Sector, blank=True)
    stakeholder_register = models.BooleanField("Has this partner been added to stakeholder register?", default=0)
    formal_relationship_document = models.ForeignKey(
        'Documentation', verbose_name="Formal Written Description of Relationship", null=True, blank=True,
        related_name="relationship_document")
    vetting_document = models.ForeignKey('Documentation', verbose_name="Vetting/ due diligence statement", null=True,
                                         blank=True, related_name="vetting_document")
    approval = models.ManyToManyField(ApprovalWorkflow, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='stakeholders', null=True, blank=True)
    # TODO: optimize query
    objects = StakeholderManager()

    class Meta:
        ordering = ('country','name','type')
        verbose_name_plural = "Stakeholders"

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Stakeholder, self).save()

    def __unicode__(self):
        return unicode(self.name)


class Partner(models.Model):
    partners_uuid = models.CharField(max_length=255, verbose_name='Partner UUID', default=uuid.uuid4, unique=True)
    name = models.CharField("Partner/Organization Name", max_length=255, blank=True, null=True)
    type = models.ForeignKey(StakeholderType, blank=True, null=True, related_name="stakeholder_partner")
    country = models.ForeignKey(Country, blank=True, null=True)
    sectors = models.ManyToManyField(Sector, blank=True)
    organization = models.ForeignKey(Organization, default=1)
    workflowlevel1 = models.ManyToManyField(WorkflowLevel1, blank=True)
    approval = models.ManyToManyField(ApprovalWorkflow, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('country','name','type')
        verbose_name_plural = "Partners"

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Partner, self).save()

    def __unicode__(self):
        return unicode(self.name)


class WorkflowLevel2Manager(models.Manager):
    def get_approved(self):
        return self.filter(status="approved")

    def get_open(self):
        return self.filter(status="")

    def get_inprogress(self):
        return self.filter(status="in progress")

    def get_awaiting_approval(self):
        return self.filter(status="awaiting approval")

    def get_new(self):
        return self.filter(Q(approval=None) | Q(approval=""))

    def get_queryset(self):
        return super(WorkflowLevel2Manager, self).get_queryset().select_related('office')


class WorkflowLevel2(models.Model):
    actual_start_date = models.DateTimeField(blank=True, null=True)
    actual_end_date = models.DateTimeField(blank=True, null=True)
    actual_duration = models.CharField(max_length=255, blank=True, null=True)
    actual_cost = models.DecimalField("Actual Cost", decimal_places=2, max_digits=20, default=Decimal("0.00"), blank=True, help_text="Cost to date calculated from Budget Module")
    address = HStoreField(blank=True, null=True, help_text="Address object with the structure: street (string), house_number (string), postal_code: (string), city (string), country (string)")
    capacity_built = models.TextField("Describe how sustainability was ensured for this project?", max_length=755, blank=True, null=True, help_text="Descriptive, did this help increases internal or external capacity")
    description = models.TextField("Description", blank=True, null=True, help_text="Description of the overall effort")
    description_of_community_involvement = models.TextField(blank=True, null=True, help_text="Descriptive, what community orgs are groups are involved")
    description_of_government_involvement = models.TextField(blank=True, null=True, help_text="Descriptive, what government entities might be involved")
    expected_end_date = models.DateTimeField("Expected ending date", blank=True, null=True)
    expected_start_date = models.DateTimeField("Expected starting date", blank=True, null=True)
    issues_and_challenges = models.TextField("List any issues or challenges faced (include reasons for delays)", blank=True, null=True, help_text="Descriptive, what are some of the issues and challenges")
    justification_background = models.TextField("General Background and Problem Statement", blank=True, null=True, help_text="Descriptive, why are we starting this effort")
    lessons_learned = models.TextField("Lessons learned", blank=True, null=True, help_text="Descriptive, when completed what lessons were learned")
    level2_uuid = models.CharField(max_length=255, editable=False, verbose_name='WorkflowLevel2 UUID', default=uuid.uuid4, unique=True, blank=True, help_text="Unique ID")
    name = models.CharField("Name", max_length=255)
    notes = models.TextField(blank=True, null=True)
    parent_workflowlevel2 = models.IntegerField("Parent", default=0, blank=True)
    quality_assured = models.TextField("How was quality assured for this project", max_length=755, blank=True, null=True, help_text="Descriptive, how was the overall quality assured for this effort")
    risks_assumptions = models.TextField("Risks and Assumptions", blank=True, null=True, help_text="Descriptive, what are the risks associated")
    short_name = models.CharField("Code", max_length=20, blank=True, null=True, help_text="Shortened name autogenerated")
    site_instructions = models.TextField(blank=True, null=True)
    total_cost = models.DecimalField("Estimated Budget for Organization", decimal_places=2, max_digits=12, help_text="In USD", default=Decimal("0.00"), blank=True)
    total_estimated_budget = models.DecimalField("Total Project Budget", decimal_places=2, max_digits=12, help_text="Total budget to date calculated from Budget Module", default=Decimal("0.00"), blank=True)
    type = models.CharField(max_length=50, blank=True, null=True)

    approval = models.ManyToManyField(ApprovalWorkflow, blank=True, help_text="Multiple approval level and users")
    donor_currency = models.ForeignKey(Currency, null=True, blank=True, related_name="donor_project", on_delete=models.SET_NULL, help_text="Secondary Currency")
    effect_or_impact = models.TextField("What is the anticipated Outcome or Goal?", blank=True, null=True, help_text="Descriptive, what is the anticipated outcome of the effort")
    indicators = models.ManyToManyField("indicators.Indicator", blank=True)
    local_currency = models.ForeignKey(Currency, null=True, blank=True, related_name="local_project", on_delete=models.SET_NULL, help_text="Primary Currency")
    milestone = models.ForeignKey("Milestone", null=True, blank=True, on_delete=models.SET_NULL, help_text="Association with a Workflow Level 1 Milestone")
    office = models.ForeignKey(Office, verbose_name="Office", null=True, blank=True, on_delete=models.SET_NULL, help_text="Primary office for effort")
    # products = OneToMany(Product)  # reverse related relationship
    sector = models.ForeignKey("Sector", verbose_name="Sector", blank=True, null=True, related_name="workflow2_sector", on_delete=models.SET_NULL, help_text="Primary Sector or type of work")
    site = models.ManyToManyField(SiteProfile, blank=True, help_text="Geographic sites or locations")
    staff_responsible = models.ForeignKey(TolaUser, on_delete=models.SET_NULL, blank=True, null=True, help_text="Responsible party")
    stakeholder = models.ManyToManyField(Stakeholder, verbose_name="Stakeholders", blank=True, help_text="Other parties involved in effort")
    sub_sector = models.ManyToManyField("Sector", verbose_name="Sub-Sector", blank=True, related_name="workflowlevel2_sub_sector", help_text="Secondary sector or type of work")
    workflowlevel1 = models.ForeignKey(WorkflowLevel1, verbose_name="Program", related_name="workflowlevel2", help_text="Primary Workflow")

    create_date = models.DateTimeField("Date Created", null=True, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='workflowlevel2', null=True, blank=True, on_delete=models.SET_NULL)
    edit_date = models.DateTimeField("Last Edit Date", null=True, blank=True)

    history = HistoricalRecords()
    objects = WorkflowLevel2Manager()

    STATUS_GREEN = "green"
    STATUS_YELLOW = "yellow"
    STATUS_ORANGE = "orange"
    STATUS_RED = "red"

    STATUS_CHOICES = (
        (STATUS_GREEN, "Green"),
        (STATUS_YELLOW, "Yellow"),
        (STATUS_ORANGE, "Orange"),
        (STATUS_RED, "Red")
    )

    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default="green", blank=True)

    PROGRESS_OPEN = "open"
    PROGRESS_AWAITING_APPROVAL = "awaitingapproval"
    PROGRESS_TRACKING = "tracking"
    PROGRESS_IN_PROGRESS = "inprogress"
    PROGRESS_INVOICED = "invoiced"
    PROGRESS_CLOSED = "closed"

    PROGRESS_CHOICES = (
        (PROGRESS_OPEN, "Open"),
        (PROGRESS_AWAITING_APPROVAL, "Awaiting Approval"),
        (PROGRESS_TRACKING, "Tracking"),
        (PROGRESS_IN_PROGRESS, "In Progress"),
        (PROGRESS_INVOICED, "Invoiced"),
        (PROGRESS_CLOSED, "Closed")
    )

    progress = models.CharField(choices=PROGRESS_CHOICES, max_length=50,
                                default="open", blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Workflow Level 2"
        verbose_name_plural = "Workflow Level 2"
        permissions = (
            ("can_approve", "Can approve initiation"),
        )

    def _validate_address(self, address):
        schema = Schema({
            'street': All(Any(str, unicode), Length(max=100)),
            'house_number': All(Any(str, unicode), Length(max=20)),
            'postal_code': All(Any(str, unicode), Length(max=20)),
            'city': All(Any(str, unicode), Length(max=85)),
            'country': All(Any(str, unicode), Length(max=50)),
        })
        schema(address)

    def clean_fields(self, exclude=None):
        super(WorkflowLevel2, self).clean_fields(exclude=exclude)
        if self.address:
            try:
                self._validate_address(self.address)
            except Exception as error:
                raise ValidationError(error)

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()

        # defaults don't work if they aren't in the form so preset these to 0
        if self.total_estimated_budget is None:
            self.total_estimated_budget = Decimal("0.00")
        if self.total_cost is None:
            self.total_cost = Decimal("0.00")

        super(WorkflowLevel2, self).save(*args, **kwargs)

        ei = ElasticsearchIndexer()
        ei.index_workflowlevel2(self)

    def delete(self, *args, **kwargs):
        super(WorkflowLevel2, self).delete(*args, **kwargs)

        ei = ElasticsearchIndexer()
        ei.delete_workflowlevel2(self)

    @property
    def project_name_clean(self):
        return self.name.encode('ascii', 'ignore')

    @property
    def sites(self):
        return ', '.join([x.name for x in self.site.all()])

    @property
    def stakeholders(self):
        return ', '.join([x.name for x in self.stakeholder.all()])

    def __unicode__(self):
        return unicode(self.name)


class WorkflowLevel2Sort(models.Model):
    workflowlevel1 = models.ForeignKey(WorkflowLevel1, null=True, blank=True)
    workflowlevel2_parent_id = models.ForeignKey(WorkflowLevel2, null=True, blank=True)
    workflowlevel2_id = models.IntegerField("ID to be Sorted", default=0)
    sort_array = JSONField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('workflowlevel1', 'workflowlevel2_id')
        verbose_name = "Workflow Level 2 Sort"
        verbose_name_plural = "Workflow Level 2 Sort"

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(WorkflowLevel2Sort, self).save()

    def __unicode__(self):
        return unicode(self.workflowlevel1)


class Documentation(models.Model):
    document_uuid = models.CharField(max_length=255, verbose_name='Document UUID', default=uuid.uuid4, unique=True, blank=True)
    name = models.CharField("Name of Document", max_length=255, blank=True, null=True)
    url = models.CharField("URL (Link to document or document repository)", blank=True, null=True, max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    file_field = models.FileField(upload_to="uploads", blank=True, null=True)
    file_type = models.CharField(max_length=255, blank=True, null=True)
    workflowlevel2 = models.ForeignKey(WorkflowLevel2, blank=True, null=True, related_name="doc_workflowlevel2")
    workflowlevel1 = models.ForeignKey(WorkflowLevel1)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='documentation', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Documentation, self).save()

    def __unicode__(self):
        return self.name

    @property
    def name_n_url(self):
        return "%s %s" % (self.name, self.url)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Documentation"


class Budget(models.Model):
    contributor = models.CharField(max_length=135, blank=True, null=True, help_text="Source of budget fund")
    account_code = models.CharField("Accounting Code", max_length=135, blank=True, null=True, help_text="Label or coded field")
    cost_center = models.CharField("Cost Center", max_length=135, blank=True, null=True, help_text="Associate a cost with a type of expense")
    donor_code = models.CharField("Donor Code", max_length=135, blank=True, null=True, help_text="Third Party coded field")
    description_of_contribution = models.CharField(max_length=255, blank=True, null=True, help_text="Purpose or use for funds")
    proposed_value = models.DecimalField("Budget", decimal_places=2, max_digits=12, default=Decimal("0.00"), blank=True, help_text="Approximate value if not a monetary fund")
    actual_value = models.DecimalField("Actual", decimal_places=2, max_digits=12, default=Decimal("0.00"), blank=True, help_text="Monetary value positive or negative")
    workflowlevel2 = models.ForeignKey(WorkflowLevel2, blank=True, null=True, on_delete=models.SET_NULL, help_text="Releated workflow level 2")
    local_currency = models.ForeignKey(Currency, blank=True, null=True, related_name="local", help_text="Primary Currency")
    donor_currency = models.ForeignKey(Currency, blank=True, null=True, related_name="donor", help_text="Secondary Currency")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='budgets', null=True, blank=True)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if not self.create_date:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()

        if self.proposed_value is None:
            self.proposed_value = Decimal("0.00")
        if self.actual_value is None:
            self.actual_value = Decimal("0.00")

        super(Budget, self).save()

    def __unicode__(self):
        return self.contributor

    class Meta:
        ordering = ('contributor',)


class RiskRegister(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=135, blank=True, null=True)
    impact = models.CharField(max_length=255, blank=True, null=True)
    likelihood = models.CharField(max_length=255, blank=True, null=True)
    rating = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(default=0, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    contingency_plan = models.CharField(max_length=255, blank=True, null=True)
    mitigation_plan = models.CharField(max_length=255, blank=True, null=True)
    post_mitigation_status = models.CharField(max_length=255, blank=True, null=True)
    action_by = models.DateTimeField(null=True, blank=True)
    action_when = models.DateTimeField(null=True, blank=True)
    workflowlevel2 = models.ForeignKey(WorkflowLevel2,null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(RiskRegister, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('type','name')


class IssueRegister(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=135, blank=True, null=True)
    impact = models.CharField(max_length=255, blank=True, null=True)
    rating = models.CharField(max_length=255, blank=True, null=True)
    status = models.IntegerField(default=0, blank=True, null=True)
    cause = models.CharField(max_length=255, blank=True, null=True)
    assigned = models.ForeignKey(TolaUser, blank=True, null=True)
    date_opened = models.DateTimeField(null=True, blank=True)
    date_resolved = models.DateTimeField(null=True, blank=True)
    workflowlevel2 = models.ForeignKey(WorkflowLevel2, null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True, blank=True)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(IssueRegister, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('type','name')


class WorkflowModules(models.Model):
    workflowlevel2 = models.ForeignKey("WorkflowLevel2")

    MODULES = (
        ('approval', 'Approval'),
        ('budget', 'Budget'),
        ('stakeholders', 'Stakeholders'),
        ('documents', 'Documents'),
        # in-activte for 2.0 GWL
        #('risk_issues', 'Risks and Issues'),
        ('sites', 'Sites'),
        ('indicators', 'Indicators'),
        # in-activte for 2.0 GWL
        #('procurement_plan', 'Procurement Plan'),
    )

    modules = models.CharField(choices=MODULES, max_length=50, default="open")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('modules',)
        verbose_name_plural = "Workflow Modules"

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(WorkflowModules, self).save()

    def __unicode__(self):
        return unicode(self.workflowlevel2)
