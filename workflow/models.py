from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from decimal import Decimal
from datetime import datetime
import uuid

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from simple_history.models import HistoricalRecords
from django.contrib.postgres.fields import JSONField
from django.contrib.sessions.models import Session

from django.db import migrations

try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone
from django.db.models import Q


# New user created generate a token
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class TolaSites(models.Model):
    name = models.CharField(blank=True, null=True, max_length=255)
    agency_name = models.CharField(blank=True, null=True, max_length=255)
    agency_url = models.CharField(blank=True, null=True, max_length=255)
    tola_report_url = models.CharField(blank=True, null=True, max_length=255)
    tola_tables_url = models.CharField(blank=True, null=True, max_length=255)
    tola_tables_user = models.CharField(blank=True, null=True, max_length=255)
    tola_tables_token = models.CharField(blank=True, null=True, max_length=255)
    site = models.ForeignKey(Site)
    privacy_disclaimer = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now=False, blank=True, null=True)
    updated = models.DateTimeField(auto_now=False, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Tola Sites"

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps as appropriate '''
        if kwargs.pop('new_entry', True):
            self.created = datetime.now()
        else:
            self.updated = datetime.now()
        return super(TolaSites, self).save(*args, **kwargs)


class TolaSitesAdmin(admin.ModelAdmin):
    list_display = ('name', 'agency_name')
    display = 'Tola Site'
    list_filter = ('name',)
    search_fields = ('name','agency_name')


class Organization(models.Model):
    name = models.CharField("Organization Name", max_length=255, blank=True, default="TolaData")
    description = models.TextField("Description/Notes", max_length=765, null=True, blank=True)
    organization_url = models.CharField(blank=True, null=True, max_length=255)
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
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Organization, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'edit_date')
    display = 'Organization'


class Country(models.Model):
    country = models.CharField("Country Name", max_length=255, blank=True)
    organization = models.ForeignKey(Organization, blank=True, null=True)
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
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
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
    title = models.CharField(blank=True, null=True, max_length=3, choices=TITLE_CHOICES)
    name = models.CharField("Given Name", blank=True, null=True, max_length=100)
    employee_number = models.IntegerField("Employee Number", blank=True, null=True)
    user = models.OneToOneField(User, unique=True, related_name='tola_user')
    organization = models.ForeignKey(Organization, default=1, blank=True, null=True)
    country = models.ForeignKey(Country, blank=True, null=True)
    countries = models.ManyToManyField(Country, verbose_name="Accessible Countries", related_name='countries', blank=True)
    tables_api_token = models.CharField(blank=True, null=True, max_length=255)
    activity_api_token = models.CharField(blank=True, null=True, max_length=255)
    privacy_disclaimer_accepted = models.BooleanField(default=False)
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
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(TolaUser, self).save()


class Award(models.Model):
    donors = models.ManyToManyField("Stakeholder", blank=True)
    name = models.CharField("Award Name/Title", blank=True, null=True, max_length=100)
    organization = models.ForeignKey(Organization, default=1, blank=True, null=True)
    countries = models.ManyToManyField(Country, verbose_name="Countries", related_name='countries_award', blank=True)
    amount = models.IntegerField("Amount", blank=True, default=0)

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
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Award, self).save()


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

    def __unicode__(self):
        return self.name

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(TolaBookmarks, self).save()


class TolaBookmarksAdmin(admin.ModelAdmin):

    list_display = ('user', 'name')
    display = 'Tola User Bookmarks'
    list_filter = ('user__name',)
    search_fields = ('name','user')


class TolaUserProxy(TolaUser):

    class Meta:
        verbose_name, verbose_name_plural = u"Report Tola User", u"Report Tola Users"
        proxy = True


class TolaUserAdmin(admin.ModelAdmin):

    list_display = ('name', 'country')
    display = 'Tola User'
    list_filter = ('country', 'user__is_staff',)
    search_fields = ('name','country__country','title')


# Form Guidance
class FormGuidance(models.Model):
    form = models.CharField(max_length=135,null=True, blank=True)
    guidance_link = models.URLField(max_length=200, null=True, blank=True)
    guidance = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('create_date',)

    def save(self):
        if self.create_date is None:
            self.create_date = datetime.now()
        super(FormGuidance, self).save()

    def __unicode__(self):
        return unicode(self.form)


class FormGuidanceAdmin(admin.ModelAdmin):
    list_display = ( 'form', 'guidance', 'guidance_link', 'create_date',)
    display = 'Form Guidance'


class ProjectType(models.Model):
    name = models.CharField("Type of Activity", max_length=135)
    description = models.CharField(max_length=765)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ProjectType, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'create_date', 'edit_date')
    display = 'Project Type'


class Sector(models.Model):
    sector = models.CharField("Sector Name", max_length=255, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('sector',)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Sector, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.sector


class SectorAdmin(admin.ModelAdmin):
    list_display = ('sector', 'create_date', 'edit_date')
    display = 'Sector'


class Contact(models.Model):
    name = models.CharField("Name", max_length=255, blank=True, null=True)
    title = models.CharField("Title", max_length=255, blank=True, null=True)
    city = models.CharField("City/Town", max_length=255, blank=True, null=True)
    address = models.TextField("Address", max_length=255, blank=True, null=True)
    email = models.CharField("Email", max_length=255, blank=True, null=True)
    phone = models.CharField("Phone", max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name', 'country','title')
        verbose_name_plural = "Contact"

    # onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Contact, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name + ", " + self.title


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'create_date', 'edit_date')
    display = 'Contact'
    list_filter = ('create_date','country')
    search_fields = ('name','country','title','city')


class FundCode(models.Model):
    name = models.CharField("Fund Code", max_length=255, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(FundCode, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class FundCodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'edit_date')
    display = 'Fund Code'


class Currency(models.Model):
    source_currency = models.CharField("Source Currency Name", max_length=255, blank=True)
    target_currency = models.CharField("Target Currency Name", max_length=255, blank=True)
    current_rate = models.IntegerField("Conversion Rate", null=True, blank=True)
    conversion_date = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('source_currency',)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Currency, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.source_currency


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('source_currency','target_currency', 'current_rate', 'conversion_date')
    display = 'Currency Conversion'


class ApprovalType(models.Model):
    name = models.CharField("Name", max_length=255, blank=True)
    organization = models.ForeignKey(Organization)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name','organization')

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ApprovalType, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class ApprovalTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    display = 'Approval Types'


class ApprovalWorkflow(models.Model):
    note = models.TextField(null=True, blank=True)
    approval_type = models.ForeignKey(ApprovalType, null=False, related_name="approval_type")
    assigned_to = models.ForeignKey(TolaUser, null=False, related_name="to_approval")
    requested_from = models.ForeignKey(TolaUser, null=False, related_name="from_approval")
    date_assigned = models.DateTimeField(null=True, blank=True)
    date_approved = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

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
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ApprovalWorkflow, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.approval_type)


class ApprovalWorkflowAdmin(admin.ModelAdmin):
    list_display = ('approval_type','section')
    display = 'Approval Workflow'


class WorkflowLevel1(models.Model):
    level1_uuid = models.CharField(max_length=255, verbose_name='WorkflowLevel1 UUID', default=uuid.uuid4, unique=True)
    unique_id = models.CharField("ID", max_length=255, blank=True, unique=True)
    name = models.CharField("Name", max_length=255, blank=True)
    funding_status = models.CharField("Funding Status", max_length=255, blank=True)
    cost_center = models.CharField("Fund Code", max_length=255, blank=True, null=True)
    fund_code = models.ManyToManyField(FundCode, blank=True)
    description = models.TextField("Description", max_length=765, null=True, blank=True)
    sector = models.ManyToManyField(Sector, blank=True)
    sub_sector = models.ManyToManyField(Sector, blank=True, related_name="sub_sector")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    country = models.ManyToManyField(Country)
    user_access = models.ManyToManyField(TolaUser, blank=True)
    public_dashboard = models.BooleanField("Enable Public Dashboard", default=False)
    sort = models.IntegerField(default=0)  #sort array for activities related to a project

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "WorkflowLevel1"

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if not 'force_insert' in kwargs:
            kwargs['force_insert'] = False
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(WorkflowLevel1, self).save()

    @property
    def countries(self):
        return ', '.join([x.country for x in self.country.all()])

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class WorkflowAccess(models.Model):
    workflow_user = models.ForeignKey(TolaUser,help_text='User', blank=True, null=True, related_name="auth_approving")
    workflowlevel1 = models.ManyToManyField(WorkflowLevel1, blank=True)
    role=models.TextField(null=True, blank=True)
    budget_limit = models.IntegerField(null=True, blank=True)
    country = models.ForeignKey("Country", null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('workflow_user',)
        verbose_name_plural = "WorkflowAccess"

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(WorkflowAccess, self).save()

    @property
    def workflowlevel1s(self):
        return ', '.join([x.workflowlevel1 for x in self.workflowlevel1.all()])

    # displayed in admin templates
    def __unicode__(self):
        return self.workflow_user.user.first_name + " " + self.workflow_user.user.last_name


class Province(models.Model):
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
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Province, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'create_date')
    search_fields = ('name','country__country')
    list_filter = ('create_date','country')
    display = 'Admin Boundary 1'


class District(models.Model):
    name = models.CharField("Admin Boundary 2", max_length=255, blank=True)
    province = models.ForeignKey(Province,verbose_name="Admin Level 1")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Admin Boundary 2"
        verbose_name_plural = "Admin Boundary 2"

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(District, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'create_date')
    search_fields = ('create_date','province')
    list_filter = ('province__country__country','province')
    display = 'Admin Boundary 2'


class AdminLevelThree(models.Model):
    name = models.CharField("Admin Boundary 3", max_length=255, blank=True)
    district = models.ForeignKey(District,verbose_name="Admin Level 2")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Admin Boundary 3"
        verbose_name_plural = "Admin Boundary 3"

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(AdminLevelThree, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class AdminLevelThreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'create_date')
    search_fields = ('name','district__name')
    list_filter = ('district__province__country__country','district')
    display = 'Admin Boundary 3'


class Village(models.Model):
    name = models.CharField("Admin Boundary 4", max_length=255, blank=True)
    district = models.ForeignKey(District,null=True,blank=True)
    admin_3 = models.ForeignKey(AdminLevelThree,verbose_name="Admin Boundary 3",null=True,blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = "Admin Boundary 4"
        verbose_name_plural = "Admin Boundary 4"

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Village, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class VillageAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'create_date', 'edit_date')
    list_filter = ('district__province__country__country','district')
    display = 'Admin Boundary 4'


class Office(models.Model):
    name = models.CharField("Office Name", max_length=255, blank=True)
    code = models.CharField("Office Code", max_length=255, blank=True)
    country = models.ForeignKey(Country,verbose_name="Admin Level 1")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Office, self).save()

    # displayed in admin templates
    def __unicode__(self):
        new_name = unicode(self.name) + unicode(" - ") + unicode(self.code)
        return new_name


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'country', 'create_date', 'edit_date')
    search_fields = ('name','country__country','code')
    list_filter = ('create_date','country__country')
    display = 'Office'


class ProfileType(models.Model):
    profile = models.CharField("Profile Type", max_length=255, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('profile',)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ProfileType, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.profile


class ProfileTypeAdmin(admin.ModelAdmin):
    list_display = ('profile', 'create_date', 'edit_date')
    display = 'ProfileType'


class LandType(models.Model):
    classify_land = models.CharField("Land Classification", help_text="Rural, Urban, Peri-Urban", max_length=100, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('classify_land',)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(LandType, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.classify_land


class LandTypeAdmin(admin.ModelAdmin):
    list_display = ('classify_land', 'create_date', 'edit_date')
    display = 'Land Type'


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
    province = models.ForeignKey(Province, verbose_name="Administrative Level 1", null=True, blank=True)
    district = models.ForeignKey(District, verbose_name="Administrative Level 2", null=True, blank=True)
    admin_level_three = models.ForeignKey(AdminLevelThree, verbose_name="Administrative Level 3", null=True, blank=True)
    village = models.ForeignKey(Village, verbose_name="Administrative Level 4", null=True, blank=True)
    latitude = models.DecimalField("Latitude (Decimal Coordinates)", decimal_places=16,max_digits=25, default=Decimal("0.00"))
    longitude = models.DecimalField("Longitude (Decimal Coordinates)", decimal_places=16,max_digits=25, default=Decimal("0.00"))
    status = models.BooleanField("Site Active", default=True)
    approval = models.ManyToManyField(ApprovalWorkflow, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
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
            self.create_date = datetime.now()
            self.edit_date = datetime.now()

        super(SiteProfile, self).save()

    # displayed in admin templates
    def __unicode__(self):
        new_name = self.name
        return new_name


class SiteProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'code','office', 'country', 'district', 'province', 'village', 'cluster', 'longitude', 'latitude', 'create_date', 'edit_date')
    list_filter = ('country__country')
    search_fields = ('code','office__code','country__country')
    display = 'SiteProfile'


class StakeholderType(models.Model):
    name = models.CharField("Stakeholder Type", max_length=255, blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Stakeholder Types"

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(StakeholderType, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class StakeholderTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'edit_date')
    display = 'Stakeholder Types'
    list_filter = ('create_date')
    search_fields = ('name')


class ProjectType(models.Model):
    name = models.CharField("Type of Activity", max_length=135)
    description = models.CharField(max_length=765)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ProjectType, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'create_date', 'edit_date')
    display = 'Project Type'


class Template(models.Model):
    name = models.CharField("Name of Document", max_length=135)
    documentation_type = models.CharField("Type (File or URL)", max_length=135)
    description = models.CharField(max_length=765)
    file_field = models.FileField(upload_to="uploads", blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Template, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'documentation_type', 'file_field', 'create_date', 'edit_date')
    display = 'Template'


class StakeholderManager(models.Manager):
    def get_queryset(self):
        return super(StakeholderManager, self).get_queryset().prefetch_related('contact', 'sectors').select_related('country','type','formal_relationship_document','vetting_document')


class Stakeholder(models.Model):
    stakeholder_uuid = models.CharField(max_length=255, verbose_name='Stakeholder UUID', default=uuid.uuid4, unique=True)
    name = models.CharField("Stakeholder/Organization Name", max_length=255, blank=True, null=True)
    type = models.ForeignKey(StakeholderType, blank=True, null=True)
    contact = models.ManyToManyField(Contact, max_length=255, blank=True)
    country = models.ForeignKey(Country)
    sectors = models.ManyToManyField(Sector, blank=True)
    stakeholder_register = models.BooleanField("Has this partner been added to stakeholder register?")
    formal_relationship_document = models.ForeignKey('Documentation', verbose_name="Formal Written Description of Relationship", null=True, blank=True, related_name="relationship_document")
    vetting_document = models.ForeignKey('Documentation', verbose_name="Vetting/ due diligence statement", null=True, blank=True, related_name="vetting_document")
    approval = models.ManyToManyField(ApprovalWorkflow, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    #optimize query
    objects = StakeholderManager()

    class Meta:
        ordering = ('country','name','type')
        verbose_name_plural = "Stakeholders"

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Stakeholder, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.name)


class WorkflowLevel2Manager(models.Manager):
    def get_approved(self):
        return self.filter(approval="approved")

    def get_open(self):
        return self.filter(approval="")

    def get_inprogress(self):
        return self.filter(approval="in progress")

    def get_awaiting_approval(self):
        return self.filter(approval="awaiting approval")

    def get_rejected(self):
        return self.filter(approval="rejected")

    def get_new(self):
        return self.filter(Q(approval=None) | Q(approval=""))

    def get_queryset(self):
        return super(WorkflowLevel2Manager, self).get_queryset().select_related('office')


class WorkflowLevel2(models.Model):
    """
        Releated to workflowlevel1 this is the activity piece multiple workflows2 can be created and related
        to a workflowlevel1 and configured with components
    """
    # START of Project Definition Fields
    level2_uuid = models.CharField(max_length=255, verbose_name='WorkflowLevel2 UUID', default=uuid.uuid4, unique=True)
    short = models.BooleanField(default=True, verbose_name="Short Form (recommended)")
    workflowlevel1 = models.ForeignKey(WorkflowLevel1, verbose_name="Program", related_name="workflowlevel2")
    parent_workflowlevel2 = models.IntegerField("Parent", default=0)
    date_of_request = models.DateTimeField("Date of Request", blank=True, null=True)
    # Rename to more generic "nonproject" names
    project_name = models.CharField("Project Name",
                                    help_text='Please be specific in your name.  Consider that the name includes WHO, WHAT, WHERE, HOW',
                                    max_length=255)
    project_type = models.ForeignKey(ProjectType, verbose_name="Project Type", help_text='', max_length=255, blank=True,
                                     null=True)
    project_activity = models.CharField("Project Activity",
                                        help_text='This should come directly from the activities listed in the Logframe',
                                        max_length=255, blank=True, null=True)
    project_description = models.TextField("Project Description", help_text='', blank=True, null=True)
    site = models.ManyToManyField(SiteProfile, blank=True)
    has_rej_letter = models.BooleanField("If Rejected: Rejection Letter Sent?", help_text='If yes attach copy',
                                         default=False)
    # this needs to be a smart acronym generated based on the program name and project names initials
    activity_code = models.CharField("Project Code", help_text='', max_length=255, blank=True, null=True)
    office = models.ForeignKey(Office, verbose_name="Office", null=True, blank=True)
    cod_num = models.CharField("Project COD #", max_length=255, blank=True, null=True)
    sector = models.ForeignKey("Sector", verbose_name="Sector", blank=True, null=True)
    #project_design = models.CharField("Activity design for", max_length=255, blank=True, null=True)
    account_code = models.CharField("Fund Code", help_text='', max_length=255, blank=True, null=True)
    lin_code = models.CharField("LIN Code", help_text='', max_length=255, blank=True, null=True)
    staff_responsible = models.CharField("Staff Responsible", max_length=255, blank=True, null=True)

    # TODO: It looks like Partners could be considered a separate model, here could be appended a list of partners
    partners = models.BooleanField("Are there partners involved?", default=0)
    name_of_partners = models.CharField("Name of Partners", max_length=255, blank=True, null=True)

    stakeholder = models.ManyToManyField(Stakeholder, verbose_name="Stakeholders", blank=True)
    effect_or_impact = models.TextField("What is the anticipated Outcome or Goal?", blank=True, null=True)
    expected_start_date = models.DateTimeField("Expected starting date", blank=True, null=True)
    expected_end_date = models.DateTimeField("Expected ending date", blank=True, null=True)
    expected_duration = models.CharField("Expected duration", help_text="[MONTHS]/[DAYS]", blank=True, null=True,
                                         max_length=255)
    beneficiary_type = models.CharField("Type of direct beneficiaries",
                                        help_text="i.e. Farmer, Association, Student, Govt, etc.", max_length=255,
                                        blank=True, null=True)
    estimated_num_direct_beneficiaries = models.CharField("Estimated number of direct beneficiaries",
                                                          help_text="Please provide achievable estimates as we will use these as our 'Targets'",
                                                          max_length=255, blank=True, null=True)
    # average household size is optional and could be considered additional data
    average_household_size = models.CharField("Average Household Size",
                                              help_text="Refer to Form 01 - Community Profile", max_length=255,
                                              blank=True, null=True)
    estimated_num_indirect_beneficiaries = models.CharField("Estimated Number of indirect beneficiaries",
                                                            help_text="This is a calculation - multiply direct beneficiaries by average household size",
                                                            max_length=255, blank=True, null=True)
    total_estimated_budget = models.DecimalField("Total Project Budget", decimal_places=2, max_digits=12,
                                                 help_text="In USD", default=Decimal("0.00"), blank=True)
    mc_estimated_budget = models.DecimalField("Organizations portion of Project Budget", decimal_places=2,
                                              max_digits=12, help_text="In USD", default=Decimal("0.00"), blank=True)
    local_total_estimated_budget = models.DecimalField("Estimated Total in Local Currency", decimal_places=2,
                                                       max_digits=12, help_text="In Local Currency",
                                                       default=Decimal("0.00"), blank=True)
    local_mc_estimated_budget = models.DecimalField("Estimated Organization Total in Local Currency", decimal_places=2,
                                                    max_digits=12,
                                                    help_text="Total portion of estimate for your agency",
                                                    default=Decimal("0.00"), blank=True)
    exchange_rate = models.CharField(help_text="Local Currency exchange rate to USD", max_length=255, blank=True,
                                     null=True)
    exchange_rate_date = models.DateField(help_text="Date of exchange rate", blank=True, null=True)
    estimation_date = models.DateTimeField(blank=True, null=True)
    estimated_by = models.ForeignKey(TolaUser, blank=True, null=True, verbose_name="Originated By",
                                     related_name="estimating")
    estimated_by_date = models.DateTimeField("Date Originated", null=True, blank=True)
    checked_by = models.ForeignKey(TolaUser, blank=True, null=True, related_name="checking")
    checked_by_date = models.DateTimeField("Date Checked", null=True, blank=True)
    reviewed_by = models.ForeignKey(TolaUser, verbose_name="Request review", blank=True, null=True,
                                    related_name="reviewing")
    reviewed_by_date = models.DateTimeField("Date Verified", null=True, blank=True)
    finance_reviewed_by = models.ForeignKey(TolaUser, blank=True, null=True, related_name="finance_reviewing")
    finance_reviewed_by_date = models.DateTimeField("Date Reviewed by Finance", null=True, blank=True)
    me_reviewed_by = models.ForeignKey(TolaUser, blank=True, null=True, verbose_name="M&E Reviewed by",
                                       related_name="reviewing_me")
    me_reviewed_by_date = models.DateTimeField("Date Reviewed by M&E", null=True, blank=True)
    approval = models.ManyToManyField(ApprovalWorkflow, blank=True)
    justification_background = models.TextField("General Background and Problem Statement", blank=True, null=True)
    risks_assumptions = models.TextField("Risks and Assumptions", blank=True, null=True)
    justification_description_community_selection = models.TextField("Description of Stakeholder Selection Criteria",
                                                                     blank=True, null=True)
    description_of_project_activities = models.TextField(blank=True, null=True)
    description_of_government_involvement = models.TextField(blank=True, null=True)
    description_of_community_involvement = models.TextField(blank=True, null=True)
    community_project_description = models.TextField("Describe the project you would like to be considered",
                                                     blank=True, null=True,
                                                     help_text="Description must describe how the Community Proposal meets the project criteria")
    create_date = models.DateTimeField("Date Created", null=True, blank=True)
    edit_date = models.DateTimeField("Last Edit Date", null=True, blank=True)
    history = HistoricalRecords()
    # optimize base query for all classbasedviews
    objects = WorkflowLevel2Manager()
    # END of PorjectAgreement Fields

    # START of ProjectComplete specific Fields
    actual_start_date = models.DateTimeField(blank=True, null=True)
    actual_end_date = models.DateTimeField(blank=True, null=True)
    actual_duration = models.CharField(max_length=255, blank=True, null=True)
    on_time = models.BooleanField(default=True)
    no_explanation = models.TextField("If not on time explain delay", blank=True, null=True)
    estimated_budget = models.DecimalField("Estimated Budget", decimal_places=2, max_digits=12, help_text="",
                                           default=Decimal("0.00"), blank=True)
    actual_budget = models.DecimalField("Actual Cost", decimal_places=2, max_digits=20, default=Decimal("0.00"),
                                        blank=True,
                                        help_text="What was the actual final cost?  This should match any financial documentation you have in the file.   It should be completely documented and verifiable by finance and any potential audit")
    actual_cost_date = models.DateTimeField(blank=True, null=True)
    budget_variance = models.CharField("Budget versus Actual variance", blank=True, null=True, max_length=255)
    explanation_of_variance = models.CharField("Explanation of variance", blank=True, null=True, max_length=255)
    total_cost = models.DecimalField("Estimated Budget for Organization", decimal_places=2, max_digits=12,
                                     help_text="In USD", default=Decimal("0.00"), blank=True)
    agency_cost = models.DecimalField("Actual Cost for Organization", decimal_places=2, max_digits=12,
                                      help_text="In USD", default=Decimal("0.00"), blank=True)
    local_total_cost = models.DecimalField("Actual Cost", decimal_places=2, max_digits=12,
                                           help_text="In Local Currency", default=Decimal("0.00"), blank=True)
    local_agency_cost = models.DecimalField("Actual Cost for Organization", decimal_places=2, max_digits=12,
                                            help_text="In Local Currency", default=Decimal("0.00"), blank=True)
    community_handover = models.BooleanField("CommunityHandover/Sustainability Maintenance Plan",
                                             help_text='Check box if it was completed', default=False)
    capacity_built = models.TextField("Describe how sustainability was ensured for this project?", max_length=755,
                                      blank=True, null=True)
    quality_assured = models.TextField("How was quality assured for this project", max_length=755, blank=True,
                                       null=True)
    issues_and_challenges = models.TextField("List any issues or challenges faced (include reasons for delays)",
                                             blank=True, null=True)
    lessons_learned = models.TextField("Lessons learned", blank=True, null=True)
    sort = models.IntegerField(default=0)  # sort array for activities related to a project
    # END of ProjectComplete Fields

    STATUS_OPEN = "open"
    STATUS_AWAITING_APPROVAL = "awaiting_approval"
    STATUS_TRACKING = "tracking"
    STATUS_CLOSED = "closed"

    STATUS_CHOICES = (
        (STATUS_OPEN,"Open"),
        (STATUS_AWAITING_APPROVAL,"Awaiting Approval"),
        (STATUS_TRACKING,"Tracking"),
        (STATUS_CLOSED,"Closed")
    )

    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default="open")

    class Meta:
        ordering = ('project_name',)
        verbose_name_plural = "WorkflowLevel2"
        permissions = (
            ("can_approve", "Can approve initiation"),
        )

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()

        # defaults don't work if they aren't in the form so preset these to 0
        if self.total_estimated_budget == None:
            self.total_estimated_budget = Decimal("0.00")
        if self.mc_estimated_budget == None:
            self.mc_estimated_budget = Decimal("0.00")
        if self.local_total_estimated_budget == None:
            self.local_total_estimated_budget = Decimal("0.00")
        if self.local_mc_estimated_budget == None:
            self.local_mc_estimated_budget = Decimal("0.00")
        if self.estimated_budget == None:
            self.estimated_budget = Decimal("0.00")
        if self.actual_budget == None:
            self.actual_budget = Decimal("0.00")
        if self.total_cost == None:
            self.total_cost = Decimal("0.00")
        if self.agency_cost == None:
            self.agency_cost = Decimal("0.00")
        if self.local_total_cost == None:
            self.local_total_cost = Decimal("0.00")
        if self.local_agency_cost == None:
            self.local_agency_cost = Decimal("0.00")

        super(WorkflowLevel2, self).save()

    @property
    def project_name_clean(self):
        return self.project_name.encode('ascii', 'ignore')

    @property
    def sites(self):
        return ', '.join([x.name for x in self.site.all()])

    @property
    def stakeholders(self):
        return ', '.join([x.name for x in self.stakeholder.all()])

    # displayed in admin templates
    def __unicode__(self):
        new_name = unicode(self.office) + unicode(" - ") + unicode(self.project_name)
        return new_name


class Documentation(models.Model):
    document_uuid = models.CharField(max_length=255, verbose_name='Document UUID', default=uuid.uuid4, unique=True)
    name = models.CharField("Name of Document", max_length=135, blank=True, null=True)
    url = models.CharField("URL (Link to document or document repository)", blank=True, null=True, max_length=135)
    description = models.CharField(max_length=255, blank=True, null=True)
    template = models.ForeignKey(Template, blank=True, null=True)
    file_field = models.FileField(upload_to="uploads", blank=True, null=True)
    workflowlevel2 = models.ForeignKey(WorkflowLevel2, blank=True, null=True, related_name="doc_workflowlevel2")
    workflowlevel1 = models.ForeignKey(WorkflowLevel1)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

     # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
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
        verbose_name_plural = "WorkflowLevel3"

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(WorkflowLevel3, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.description


class WorkflowLevel3Admin(admin.ModelAdmin):
    list_display = ('description', 'create_date', 'edit_date')
    display = 'Workflow Level 3'


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
    history = HistoricalRecords()
    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Budget, self).save()

    def __unicode__(self):
        return self.contributor

    class Meta:
        ordering = ('contributor',)


class BudgetAdmin(admin.ModelAdmin):
    list_display = ('contributor', 'description_of_contribution', 'proposed_value', 'create_date', 'edit_date')
    display = 'Budget'


class Checklist(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True,default="Checklist")
    workflowlevel2 = models.ForeignKey(WorkflowLevel2, null=True, blank=True, verbose_name="Project Initiation")
    country = models.ForeignKey(Country,null=True,blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('workflowlevel2',)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Checklist, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.workflowlevel2)


class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('name','country')
    list_filter = ('country','workflowlevel2')


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
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ChecklistItem, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.item)


class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('item','checklist','in_file')
    list_filter = ('checklist','global_item')


class WorkflowModules(models.Model):
    workflowlevel2 = models.ForeignKey("WorkflowLevel2",max_length=255)

    MODULES = (
        ('approval', 'Approval'),
        ('budget', 'Budget'),
        ('stakeholders', 'Stakeholders'),
        ('documents', 'Documents'),
        ('risk_issues', 'Risks and Issues'),
        ('case_management', 'Case Management'),
        ('procurement_plan', 'Procurement Plan'),
    )

    modules = models.CharField(choices=MODULES, max_length=50, default="open")

    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('modules',)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(WorkflowModules, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.item)


class WorkflowModulesAdmin(admin.ModelAdmin):
    list_display = ('workflowlevel2__name',)
    list_filter = ('workflowlevel2__name',)



