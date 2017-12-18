from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from decimal import Decimal
import uuid

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from simple_history.models import HistoricalRecords
from django.contrib.postgres.fields import JSONField

from search.utils import ElasticsearchIndexer

try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone
from django.db.models import Q

ROLE_ORGANIZATION_ADMIN = 'OrgAdmin'
ROLE_PROGRAM_ADMIN = 'ProgramAdmin'
ROLE_PROGRAM_TEAM = 'ProgramTeam'
ROLE_VIEW_ONLY = 'ViewOnly'


# New user created generate a token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


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
        ''' On save, update timestamps as appropriate '''
        if kwargs.pop('new_entry', True):
            self.created = timezone.now()
        else:
            self.updated = timezone.now()
        return super(TolaSites, self).save(*args, **kwargs)


class Industry(models.Model):
    name = models.CharField("Industry Name", max_length=255, blank=True, default="TolaData")
    description = models.TextField("Description/Notes", max_length=765, null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Organizations"
        app_label = 'workflow'

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Industry, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


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

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Sector, self).save()

    # displayed in admin templates
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


class Organization(models.Model):
    organization_uuid = models.CharField(max_length=255, verbose_name='Organization UUID', default=uuid.uuid4, unique=True)
    name = models.CharField("Organization Name", max_length=255, blank=True, default="TolaData")
    description = models.TextField("Description/Notes", max_length=765, null=True, blank=True)
    organization_url = models.CharField(blank=True, null=True, max_length=255)
    industry = models.ManyToManyField(Industry, blank=True)
    sector = models.ManyToManyField(Sector, blank=True, related_name="org_sector")
    level_1_label = models.CharField("Project/Program Organization Level 1 label", default="Program", max_length=255, blank=True)
    level_2_label = models.CharField("Project/Program Organization Level 2 label", default="Project", max_length=255, blank=True)
    level_3_label = models.CharField("Project/Program Organization Level 3 label", default="Component", max_length=255, blank=True)
    level_4_label = models.CharField("Project/Program Organization Level 4 label", default="Activity", max_length=255, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Organizations"
        app_label = 'workflow'

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Organization, self).save()

    # displayed in admin templates
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

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Country, self).save()

    # displayed in admin templates
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

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Currency, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.source_currency


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

    # on save add create date or update edit date
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

    # on save add create date or update edit date
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

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(TolaBookmarks, self).save()


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

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(TolaUserFilter, self).save()


class TolaUserProxy(TolaUser):

    class Meta:
        verbose_name, verbose_name_plural = u"Report Tola User", u"Report Tola Users"
        proxy = True


# Form Guidance
class FormGuidance(models.Model):
    form = models.CharField(max_length=135,null=True, blank=True)
    guidance_link = models.URLField(max_length=200, null=True, blank=True)
    guidance = models.TextField(null=True, blank=True)
    default_global = models.BooleanField(default=0)
    organization = models.ForeignKey(Organization, default=1)
    create_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('create_date',)

    def save(self):
        if self.create_date is None:
            self.create_date = timezone.now()
        super(FormGuidance, self).save()

    def __unicode__(self):
        return unicode(self.form)


class ProjectType(models.Model):
    name = models.CharField("Type of Activity", max_length=135)
    description = models.CharField(max_length=765)
    default_global = models.BooleanField(default=0)
    organization = models.ForeignKey(Organization, default=1)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    # on save add create date or update edit date
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

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(FundCode, self).save()

    # displayed in admin templates
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

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(ApprovalType, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class ApprovalWorkflow(models.Model):
    note = models.TextField(null=True, blank=True)
    approval_type = models.ForeignKey(ApprovalType, null=False, related_name="approval_type")
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

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(ApprovalWorkflow, self).save()

    # displayed in admin templates
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

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Portfolio, self).save()

    # displayed in admin templates
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

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Milestone, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.name)


class WorkflowLevel1(models.Model):
    level1_uuid = models.CharField(max_length=255, verbose_name='WorkflowLevel1 UUID', default=uuid.uuid4, unique=True)
    unique_id = models.CharField("ID", max_length=255, blank=True, null=True)
    name = models.CharField("Name", max_length=255, blank=True)
    funding_status = models.CharField("Funding Status", max_length=255, blank=True)
    cost_center = models.CharField("Fund Code", max_length=255, blank=True, null=True)
    fund_code = models.ManyToManyField(FundCode, blank=True)
    organization = models.ForeignKey(Organization, blank=True, null=True)
    portfolio = models.ForeignKey(Portfolio, blank=True, null=True)
    award = models.ManyToManyField(Award, blank=True)
    description = models.TextField("Description", max_length=765, null=True, blank=True)
    sector = models.ManyToManyField(Sector, blank=True)
    sub_sector = models.ManyToManyField(Sector, blank=True, related_name="sub_sector")
    country = models.ManyToManyField(Country, blank=True)
    milestone = models.ManyToManyField(Milestone, blank=True)
    user_access = models.ManyToManyField(TolaUser, blank=True)
    public_dashboard = models.BooleanField("Enable Public Dashboard", default=False)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    sort = models.IntegerField(default=0)  #sort array

    class Meta:
        ordering = ('name',)
        verbose_name = "Workflow Level 1"
        verbose_name_plural = "Workflow Level 1"

    # on save add create date or update edit date
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

    # displayed in admin templates
    def __unicode__(self):
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

    # on save add create date or update edit date
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

    # displayed in admin templates
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

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(WorkflowTeam, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.workflow_user.user.first_name + " " + self.workflow_user.user.last_name


class AdminLevelOne(models.Model):
    name = models.CharField("Admin Boundary 1", max_length=255, blank=True)
    country = models.ForeignKey(Country)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Admin Boundary 1"
        verbose_name_plural = "Admin Boundary 1"

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(AdminLevelOne, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class AdminLevelTwo(models.Model):
    name = models.CharField("Admin Boundary 2", max_length=255, blank=True)
    adminlevelone = models.ForeignKey(AdminLevelOne,verbose_name="Admin Level 1")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Admin Boundary 2"
        verbose_name_plural = "Admin Boundary 2"

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(AdminLevelTwo, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class AdminLevelThree(models.Model):
    name = models.CharField("Admin Boundary 3", max_length=255, blank=True)
    adminleveltwo = models.ForeignKey(AdminLevelTwo, null=True, blank=True, verbose_name="Admin Level 2")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Admin Boundary 3"
        verbose_name_plural = "Admin Boundary 3"

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(AdminLevelThree, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class AdminLevelFour(models.Model):
    name = models.CharField("Admin Boundary 4", max_length=255, blank=True)
    adminlevelthree = models.ForeignKey(AdminLevelThree,null=True,blank=True)
    adminleveltwo = models.ForeignKey(AdminLevelTwo,verbose_name="Admin Boundary 3",null=True,blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Admin Boundary 4"
        verbose_name_plural = "Admin Boundary 4"

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(AdminLevelFour, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class Office(models.Model):
    name = models.CharField("Office Name", max_length=255, blank=True)
    code = models.CharField("Office Code", max_length=255, blank=True)
    country = models.ForeignKey(Country, verbose_name="Country")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Office, self).save()

    # displayed in admin templates
    def __unicode__(self):
        new_name = unicode(self.name) + unicode(" - ") + unicode(self.code)
        return new_name


class ProfileType(models.Model):
    profile = models.CharField("Profile Type", max_length=255, blank=True)
    default_global = models.BooleanField(default=0)
    organization = models.ForeignKey(Organization, default=1)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('profile',)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(ProfileType, self).save()

    # displayed in admin templates
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

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(LandType, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.classify_land


class SiteProfileManager(models.Manager):
    def get_queryset(self):
        return super(SiteProfileManager, self).get_queryset().prefetch_related().select_related('country','province','district','admin_level_three','type')


class SiteProfile(models.Model):
    site_uuid = models.CharField(max_length=255, verbose_name='Site UUID', default=uuid.uuid4, unique=True)
    name = models.CharField("Site Name", max_length=255, blank=False)
    type = models.ForeignKey(ProfileType, blank=True, null=True)
    office = models.ForeignKey(Office, blank=True, null=True)
    contact_leader = models.CharField("Contact Name", max_length=255, blank=True, null=True)
    date_of_firstcontact = models.DateTimeField("Date of First Contact", null=True, blank=True)
    contact_number = models.CharField("Contact Number", max_length=255, blank=True, null=True)
    num_members = models.CharField("Number of Members", max_length=255, blank=True, null=True)
    info_source = models.CharField("Data Source",max_length=255, blank=True, null=True)
    total_num_households = models.IntegerField("Total # Households", help_text="", null=True, blank=True)
    avg_household_size = models.DecimalField("Average Household Size", decimal_places=14,max_digits=25, default=Decimal("0.00"), null=True, blank=True)
    total_population = models.IntegerField(null=True, blank=True)
    total_male = models.IntegerField(null=True, blank=True)
    total_female = models.IntegerField(null=True, blank=True)
    classify_land = models.ForeignKey(LandType, blank=True, null=True)
    total_land = models.IntegerField("Total Land", help_text="In hectares/jeribs", null=True, blank=True)
    total_agricultural_land = models.IntegerField("Total Agricultural Land", help_text="In hectares/jeribs", null=True, blank=True)
    total_rainfed_land = models.IntegerField("Total Rain-fed Land", help_text="In hectares/jeribs", null=True, blank=True)
    total_horticultural_land = models.IntegerField("Total Horticultural Land", help_text="In hectares/jeribs", null=True, blank=True)
    total_literate_peoples = models.IntegerField("Total Literate People", help_text="", null=True, blank=True)
    literate_males = models.IntegerField("% of Literate Males", help_text="%", null=True, blank=True)
    literate_females = models.IntegerField("% of Literate Females", help_text="%", null=True, blank=True)
    literacy_rate = models.IntegerField("Literacy Rate (%)", help_text="%", null=True, blank=True)
    populations_owning_land = models.IntegerField("Households Owning Land", help_text="(%)", null=True, blank=True)
    avg_landholding_size = models.DecimalField("Average Landholding Size", decimal_places=14,max_digits=25, help_text="In hectares/jeribs", default=Decimal("0.00"))
    households_owning_livestock = models.IntegerField("Households Owning Livestock", help_text="(%)", null=True, blank=True)
    animal_type = models.CharField("Animal Types", help_text="List Animal Types", max_length=255, null=True, blank=True)
    country = models.ForeignKey(Country)
    province = models.ForeignKey(AdminLevelOne, verbose_name="Administrative Level 1", null=True, blank=True)
    district = models.ForeignKey(AdminLevelTwo, verbose_name="Administrative Level 2", null=True, blank=True)
    admin_level_three = models.ForeignKey(AdminLevelThree, verbose_name="Administrative Level 3", null=True, blank=True, related_name="site_level3")
    village = models.ForeignKey(AdminLevelThree, verbose_name="Administrative Level 4", null=True, blank=True)
    latitude = models.DecimalField("Latitude (Decimal Coordinates)", decimal_places=16,max_digits=25, default=Decimal("0.00"))
    longitude = models.DecimalField("Longitude (Decimal Coordinates)", decimal_places=16,max_digits=25, default=Decimal("0.00"))
    status = models.BooleanField("Site Active", default=True)
    approval = models.ManyToManyField(ApprovalWorkflow, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True, blank=True)
    workflowlevel1 = models.ManyToManyField(WorkflowLevel1, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='sites', null=True, blank=True)
    history = HistoricalRecords()
    #optimize query
    objects = SiteProfileManager()

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Site Profiles"

    # on save add create date or update edit date
    def save(self, *args, **kwargs):

        # Check if a create date has been specified. If not, display today's date in create_date and edit_date
        if self.create_date == None:
            self.create_date = timezone.now()
            self.edit_date = timezone.now()

        super(SiteProfile, self).save()

    # displayed in admin templates
    def __unicode__(self):
        new_name = self.name
        return new_name


class Contact(models.Model):
    """
    A contact is a person or entity who may be approached for information or assistance about a Site.

    Example: Building Maintenance Manager at a Training Center.
    """
    name = models.CharField("Name", max_length=255, blank=True, null=True)
    title = models.CharField("Title", max_length=255, blank=True, null=True)
    city = models.CharField("City/Town", max_length=255, blank=True, null=True)
    address = models.TextField("Address", max_length=255, blank=True, null=True)
    email = models.CharField("Email", max_length=255, blank=True, null=True)
    phone = models.CharField("Phone", max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country)
    organization = models.ForeignKey(Organization, blank=True, null=True)
    workflowlevel1 = models.ForeignKey(WorkflowLevel1, blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name', 'country', 'title')
        verbose_name_plural = "Contact"

    # onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Contact, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name + ", " + self.title


class StakeholderType(models.Model):
    name = models.CharField("Stakeholder Type", max_length=255, blank=True, null=True)
    default_global = models.BooleanField(default=0)
    organization = models.ForeignKey(Organization, default=1)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Stakeholder Types"

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(StakeholderType, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class StakeholderManager(models.Manager):
    def get_queryset(self):
        return super(StakeholderManager, self).get_queryset().prefetch_related('contact', 'sectors').select_related(
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
    contact = models.ManyToManyField(Contact, max_length=255, blank=True)
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

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Stakeholder, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.name)


class Partner(models.Model):
    partners_uuid = models.CharField(max_length=255, verbose_name='Partner UUID', default=uuid.uuid4, unique=True)
    name = models.CharField("Partner/Organization Name", max_length=255, blank=True, null=True)
    type = models.ForeignKey(StakeholderType, blank=True, null=True, related_name="stakeholder_partner")
    contact = models.ManyToManyField(Contact, max_length=255, blank=True)
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

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Partner, self).save()

    # displayed in admin templates
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
    """
        Releated to workflowlevel1 this is the activity piece multiple
        workflows2 can be created and related to a workflowlevel1 and
        configured with components
    """
    # START of Project Definition Fields
    level2_uuid = models.CharField(max_length=255, verbose_name='WorkflowLevel2 UUID', default=uuid.uuid4, unique=True, blank=True)
    short = models.BooleanField(default=True, verbose_name="Short Form (recommended)")
    workflowlevel1 = models.ForeignKey(WorkflowLevel1, verbose_name="Program", related_name="workflowlevel2")
    parent_workflowlevel2 = models.IntegerField("Parent", default=0, blank=True)
    milestone = models.ForeignKey("Milestone", null=True, blank=True, on_delete=models.SET_NULL)
    date_of_request = models.DateTimeField("Date of Request", blank=True, null=True)
    name = models.CharField("Name",max_length=255)
    sector = models.ForeignKey("Sector", verbose_name="Sector", blank=True, null=True, related_name="workflow2_sector", on_delete=models.SET_NULL)
    sub_sector = models.ManyToManyField("Sector", verbose_name="Sub-Sector", blank=True, related_name="workflowlevel2_sub_sector")
    description = models.TextField("Description", help_text='', blank=True, null=True)
    site = models.ManyToManyField(SiteProfile, blank=True)
    # this needs to be a smart acronym generated based on
    # the program name and project names initials
    short_name = models.CharField("Code", help_text='', max_length=20, blank=True, null=True)
    office = models.ForeignKey(Office, verbose_name="Office", null=True, blank=True, on_delete=models.SET_NULL)
    staff_responsible = models.ForeignKey(TolaUser, on_delete=models.SET_NULL, blank=True, null=True)
    partners = models.ForeignKey(Partner, blank=True, null=True, verbose_name="Partners", on_delete=models.SET_NULL)
    stakeholder = models.ManyToManyField(Stakeholder, verbose_name="Stakeholders", blank=True)
    effect_or_impact = models.TextField("What is the anticipated Outcome or Goal?", blank=True, null=True)
    expected_start_date = models.DateTimeField("Expected starting date", blank=True, null=True)
    expected_end_date = models.DateTimeField("Expected ending date", blank=True, null=True)
    total_estimated_budget = models.DecimalField("Total Project Budget", decimal_places=2, max_digits=12, help_text="In USD", default=Decimal("0.00"), blank=True)
    local_currency = models.ForeignKey(Currency, null=True, blank=True, related_name="local_project", on_delete=models.SET_NULL)
    donor_currency = models.ForeignKey(Currency, null=True, blank=True, related_name="donor_project", on_delete=models.SET_NULL)
    approval = models.ManyToManyField(ApprovalWorkflow, blank=True)
    justification_background = models.TextField("General Background and Problem Statement", blank=True, null=True)
    risks_assumptions = models.TextField("Risks and Assumptions", blank=True, null=True)
    description_of_government_involvement = models.TextField(blank=True, null=True)
    description_of_community_involvement = models.TextField(blank=True, null=True)
    actual_start_date = models.DateTimeField(blank=True, null=True)
    actual_end_date = models.DateTimeField(blank=True, null=True)
    actual_duration = models.CharField(max_length=255, blank=True, null=True)
    on_time = models.BooleanField(default=True)
    no_explanation = models.TextField("If not on time explain delay", blank=True, null=True)
    actual_cost = models.DecimalField("Actual Cost", decimal_places=2, max_digits=20, default=Decimal("0.00"), blank=True, help_text="What was the actual final cost? This should match any financial documentation you have in the file. It should be completely documented and verifiable by finance and any potential audit")
    actual_cost_date = models.DateTimeField(blank=True, null=True)
    budget_variance = models.CharField("Budget versus Actual variance", blank=True, null=True, max_length=255)
    explanation_of_variance = models.CharField("Explanation of variance", blank=True, null=True, max_length=255)
    total_cost = models.DecimalField("Estimated Budget for Organization", decimal_places=2, max_digits=12, help_text="In USD", default=Decimal("0.00"), blank=True)
    agency_cost = models.DecimalField("Actual Cost for Organization", decimal_places=2, max_digits=12, help_text="In USD", default=Decimal("0.00"), blank=True)
    community_handover = models.BooleanField("CommunityHandover/Sustainability Maintenance Plan", help_text='Check box if it was completed', default=False)
    capacity_built = models.TextField("Describe how sustainability was ensured for this project?", max_length=755, blank=True, null=True)
    quality_assured = models.TextField("How was quality assured for this project", max_length=755, blank=True, null=True)
    issues_and_challenges = models.TextField("List any issues or challenges faced (include reasons for delays)", blank=True, null=True)
    lessons_learned = models.TextField("Lessons learned", blank=True, null=True)
    indicators = models.ManyToManyField("indicators.Indicator", blank=True)
    # sort array for activities related to a project
    sort = models.IntegerField(default=0, blank=True)
    create_date = models.DateTimeField("Date Created", null=True, blank=True)
    edit_date = models.DateTimeField("Last Edit Date", null=True, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='workflowlevel2', null=True, blank=True, on_delete=models.SET_NULL)
    history = HistoricalRecords()
    # optimize base query for all classbasedviews
    objects = WorkflowLevel2Manager()

    STATUS_GREEN = "green"
    STATUS_YELLOW = "yellow"
    STATUS_ORANGE = "orange"
    STATUS_RED = "red"

    STATUS_CHOICES = (
        (STATUS_GREEN,"Green"),
        (STATUS_YELLOW,"Yellow"),
        (STATUS_ORANGE,"Orange"),
        (STATUS_RED,"Red")
    )

    status = models.CharField(choices=STATUS_CHOICES, max_length=50,
                              default="green", blank=True)

    PROGRESS_OPEN = "open"
    PROGRESS_AWAITING_APPROVAL = "awaitingapproval"
    PROGRESS_TRACKING = "tracking"
    PROGRESS_CLOSED = "closed"

    PROGRESS_CHOICES = (
        (PROGRESS_OPEN,"Open"),
        (PROGRESS_AWAITING_APPROVAL,"Awaiting Approval"),
        (PROGRESS_TRACKING,"Tracking"),
        (PROGRESS_CLOSED,"Closed")
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

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()

        # defaults don't work if they aren't in the form so preset these to 0
        if self.total_estimated_budget == None:
            self.total_estimated_budget = Decimal("0.00")
        if self.total_cost == None:
            self.total_cost = Decimal("0.00")
        if self.agency_cost == None:
            self.agency_cost = Decimal("0.00")

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

    # displayed in admin templates
    def __unicode__(self):
        new_name = unicode(self.office) + unicode(" - ") + unicode(self.name)
        return new_name


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

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(WorkflowLevel2Sort, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.workflowlevel1)


class CodedField(models.Model):
    name = models.CharField("Field Name", max_length=255, blank=True, null=True)
    label = models.CharField("Field Label", max_length=255, blank=True, null=True)
    is_required = models.BooleanField("Required Field?", default=0)
    is_universal = models.BooleanField("Available in Every Level 2 Form?", default=0)
    type = models.CharField("Field Type", max_length=255, blank=True, null=True)
    organization = models.ForeignKey(Organization, default=1)
    default_value = models.CharField("Field Default Value", max_length=255, blank=True, null=True)
    api_url = models.CharField("Associated API URL", max_length=255, blank=True, null=True)
    api_token = models.CharField("Associated API Token", max_length=255, blank=True, null=True)
    workflowlevel2 = models.ManyToManyField(WorkflowLevel2, blank=True)
    workflowlevel1 = models.ManyToManyField(WorkflowLevel1, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name', 'type')
        verbose_name_plural = "CodedFields"

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(CodedField, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.name)


class CodedFieldValues(models.Model):
    value = models.CharField("Value", null=True, blank=True, max_length=255)
    coded_field = models.ForeignKey(CodedField)
    workflowlevel2 = models.ForeignKey(WorkflowLevel2, null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('value', 'coded_field', 'workflowlevel2__name')
        verbose_name_plural = "CodedFields"

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(CodedFieldValues, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.value)


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

     # on save add create date or update edit date
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


class WorkflowLevel3(models.Model):
    level3_uuid = models.CharField(max_length=255, verbose_name='WorkflowLevel3 UUID', default=uuid.uuid4, unique=True)
    percent_complete = models.IntegerField("% complete", blank=True, null=True)
    percent_cumulative = models.IntegerField("% cumulative completion", blank=True, null=True)
    est_start_date = models.DateTimeField(null=True, blank=True)
    est_end_date = models.DateTimeField(null=True, blank=True)
    actual_start_date = models.DateTimeField(null=True, blank=True)
    actual_end_date = models.DateTimeField(null=True, blank=True)
    site = models.ForeignKey(SiteProfile, null=True, blank=True)
    budget = models.IntegerField("Estimated Budget", blank=True, null=True)
    cost = models.IntegerField("Actual Cost", blank=True, null=True)
    description = models.CharField("Description", max_length=255, blank=True)
    workflowlevel2 = models.ForeignKey(WorkflowLevel2, blank=True, null=True, verbose_name="Project")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('description',)
        verbose_name = "Workflow Level 3"
        verbose_name_plural = "Workflow Level 3"

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(WorkflowLevel3, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.description


class Budget(models.Model):
    contributor = models.CharField(max_length=135, blank=True, null=True)
    account_code = models.CharField("Accounting Code",max_length=135, blank=True, null=True)
    cost_center = models.CharField("Cost Center",max_length=135, blank=True, null=True)
    donor_code = models.CharField("Donor Code",max_length=135, blank=True, null=True)
    description_of_contribution = models.CharField(max_length=255, blank=True, null=True)
    proposed_value = models.IntegerField("Budget",default=0, blank=True, null=True)
    actual_value = models.IntegerField("Actual", default=0, blank=True, null=True)
    workflowlevel2 = models.ForeignKey(WorkflowLevel2, blank=True, null=True, on_delete=models.SET_NULL)
    local_currency = models.ForeignKey(Currency, blank=True, null=True, related_name="local")
    donor_currency = models.ForeignKey(Currency, blank=True, null=True, related_name="donor")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='budgets', null=True, blank=True)
    history = HistoricalRecords()

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if not self.create_date:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()

        if self.workflowlevel2:
            wflvl2 = self.workflowlevel2
            try:
                old_budget = self.__class__.objects.get(id=self.id)
                # Subtract the old values
                wflvl2.total_estimated_budget -= old_budget.proposed_value
                wflvl2.actual_cost -= old_budget.actual_value
            except Budget.DoesNotExist:
                pass
            finally:
                # Sum the new values
                wflvl2.total_estimated_budget += self.proposed_value
                wflvl2.actual_cost += self.actual_value
                wflvl2.save()

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

    # on save add create date or update edit date
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

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(IssueRegister, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('type','name')


class Checklist(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True,default="Checklist")
    workflowlevel2 = models.ForeignKey(WorkflowLevel2, null=True, blank=True, verbose_name="Project Initiation")
    owner = models.ForeignKey(TolaUser, null=True, blank=True)
    country = models.ForeignKey(Country,null=True,blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('workflowlevel2',)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Checklist, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.workflowlevel2)


class ChecklistItem(models.Model):
    item = models.CharField(max_length=255)
    checklist = models.ForeignKey(Checklist)
    in_file = models.BooleanField(default=False)
    not_applicable = models.BooleanField(default=False)
    global_item = models.BooleanField(default=False)
    owner = models.ForeignKey(TolaUser, null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('item',)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(ChecklistItem, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.item)


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

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(WorkflowModules, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.workflowlevel2)



