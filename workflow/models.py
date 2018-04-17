from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from decimal import Decimal
from datetime import datetime
import uuid

from django.utils.translation import ugettext_lazy as _

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from simple_history.models import HistoricalRecords
from django.contrib.sessions.models import Session
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
    name = models.CharField(_("Name"), blank=True, null=True, max_length=255)
    agency_name = models.CharField(_("Agency name"), blank=True, null=True, max_length=255)
    agency_url = models.CharField(_("Agency url"), blank=True, null=True, max_length=255)
    tola_report_url = models.CharField(_("Tola report url"), blank=True, null=True, max_length=255)
    tola_tables_url = models.CharField(_("Tola tables url"), blank=True, null=True, max_length=255)
    tola_tables_user = models.CharField(_("Tola tables user"), blank=True, null=True, max_length=255)
    tola_tables_token = models.CharField(_("Tola tables token"), blank=True, null=True, max_length=255)
    site = models.ForeignKey(Site, verbose_name=_("Site"))
    privacy_disclaimer = models.TextField(_("Privacy disclaimer"), blank=True, null=True)
    created = models.DateTimeField(_("Created"), auto_now=False, blank=True, null=True)
    updated = models.DateTimeField(_("Updated"), auto_now=False, blank=True, null=True)

    class Meta:
        verbose_name_plural = _("Tola Sites")

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        ''' On save, update timestamps as appropriate '''
        if kwargs.pop('new_entry', True):
            self.created = timezone.now()
        else:
            self.updated = timezone.now()
        return super(TolaSites, self).save(*args, **kwargs)


class TolaSitesAdmin(admin.ModelAdmin):
    list_display = ('name', 'agency_name')
    display = 'Tola Site'
    list_filter = ('name',)
    search_fields = ('name','agency_name')


class Organization(models.Model):
    name = models.CharField(_("Organization Name"), max_length=255, blank=True, default="TolaData")
    description = models.TextField(_("Description/Notes"), max_length=765, null=True, blank=True)
    organization_url = models.CharField(_("Organization url"), blank=True, null=True, max_length=255)
    level_1_label = models.CharField(_("Project/Program Organization Level 1 label"), default="Program", max_length=255, blank=True)
    level_2_label = models.CharField(_("Project/Program Organization Level 2 label"), default="Project", max_length=255, blank=True)
    level_3_label = models.CharField(_("Project/Program Organization Level 3 label"), default="Component", max_length=255, blank=True)
    level_4_label = models.CharField(_("Project/Program Organization Level 4 label"), default="Activity", max_length=255, blank=True)
    create_date = models.DateTimeField(_("Create date"), null=True, blank=True)
    edit_date = models.DateTimeField(_("Edit date"), null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = _("Organizations")
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


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'edit_date')
    display = 'Organization'


class Country(models.Model):
    country = models.CharField(_("Country Name"), max_length=255, blank=True)
    organization = models.ForeignKey(Organization, blank=True, null=True, verbose_name=_("organization"))
    code = models.CharField(_("2 Letter Country Code"), max_length=4, blank=True)
    description = models.TextField(_("Description/Notes"), max_length=765,blank=True)
    latitude = models.CharField(_("Latitude"), max_length=255, null=True, blank=True)
    longitude = models.CharField(_("Longitude"), max_length=255, null=True, blank=True)
    zoom = models.IntegerField(_("Zoom"), default=5)
    create_date = models.DateTimeField(_("Create date"), null=True, blank=True)
    edit_date = models.DateTimeField(_("Edit date"), null=True, blank=True)

    class Meta:
        ordering = ('country',)
        verbose_name_plural = _("Countries")
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
    (_('mr'), _('Mr.')),
    (_('mrs'), _('Mrs.')),
    (_('ms'), _('Ms.')),
)


class TolaUser(models.Model):
    title = models.CharField(_("Title"), blank=True, null=True, max_length=3, choices=TITLE_CHOICES)
    name = models.CharField(_("Given Name"), blank=True, null=True, max_length=100)
    employee_number = models.IntegerField(_("Employee Number"), blank=True, null=True)
    user = models.OneToOneField(User, unique=True, related_name='tola_user', verbose_name=_("User"))
    organization = models.ForeignKey(Organization, default=1, blank=True, null=True, verbose_name=_("Organization"))
    country = models.ForeignKey(Country, blank=True, null=True, verbose_name=_("Country"))
    countries = models.ManyToManyField(Country, verbose_name=_("Accessible Countries"), related_name='countries', blank=True)
    tables_api_token = models.CharField(blank=True, null=True, max_length=255)
    activity_api_token = models.CharField(blank=True, null=True, max_length=255)
    privacy_disclaimer_accepted = models.BooleanField(default=False)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name=_("Tola User")
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
        super(TolaUser, self).save()


class TolaBookmarks(models.Model):
    user = models.ForeignKey(TolaUser, related_name='tolabookmark', verbose_name=_("User"))
    name = models.CharField(_("Name"), blank=True, null=True, max_length=255)
    bookmark_url = models.CharField(_("Bookmark url"), blank=True, null=True, max_length=255)
    program = models.ForeignKey("Program", blank=True, null=True, verbose_name=_("Program"))
    create_date = models.DateTimeField(_("Create date"), null=True, blank=True)
    edit_date = models.DateTimeField(_("Edit date"), null=True, blank=True)

    class Meta:
        verbose_name=_("Tola Bookmarks")
        ordering = ('name',)

    def __unicode__(self):
        return self.name

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
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
    form = models.CharField(_("Form"), max_length=135,null=True, blank=True)
    guidance_link = models.URLField(max_length=200, null=True, blank=True)
    guidance = models.TextField(_("Guidance"), null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name=_("Form Guidance")
        ordering = ('create_date',)

    def save(self):
        if self.create_date is None:
            self.create_date = timezone.now()
        super(FormGuidance, self).save()

    def __unicode__(self):
        return unicode(self.form)


class FormGuidanceAdmin(admin.ModelAdmin):
    list_display = ( 'form', 'guidance', 'guidance_link', 'create_date',)
    display = 'Form Guidance'


class Sector(models.Model):
    sector = models.CharField(_("Sector Name"), max_length=255, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name=_("Sector")
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


class SectorAdmin(admin.ModelAdmin):
    list_display = ('sector', 'create_date', 'edit_date')
    display = 'Sector'


class Contact(models.Model):
    name = models.CharField(_("Name"), max_length=255, blank=True, null=True)
    title = models.CharField(_("Title"), max_length=255, blank=True, null=True)
    city = models.CharField(_("City/Town"), max_length=255, blank=True, null=True)
    address = models.TextField(_("Address"), max_length=255, blank=True, null=True)
    email = models.CharField(_("Email"), max_length=255, blank=True, null=True)
    phone = models.CharField(_("Phone"), max_length=255, blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name=_("Country"))
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name', 'country','title')
        verbose_name_plural = _("Contact")

    # onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Contact, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return u'%s, %s' % (self.name, self.title)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'create_date', 'edit_date')
    display = 'Contact'
    list_filter = ('create_date','country')
    search_fields = ('name','country','title','city')


# For programs that have custom dashboards. The default dashboard for all other programs is 'Program Dashboard'
class FundCode(models.Model):
    name = models.CharField(_("Fund Code"), max_length=255, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name=_("Fund Code")
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


class FundCodeAdmin(admin.ModelAdmin):
    list_display = ('name','program__name', 'create_date', 'edit_date')
    display = 'Fund Code'


class Program(models.Model):
    gaitid = models.CharField(_("ID"), max_length=255, blank=True, unique=True)
    name = models.CharField(_("Program Name"), max_length=255, blank=True)
    funding_status = models.CharField(_("Funding Status"), max_length=255, blank=True)
    cost_center = models.CharField(_("Fund Code"), max_length=255, blank=True, null=True)
    fund_code = models.ManyToManyField(FundCode, blank=True, verbose_name=_("Fund code"))
    description = models.TextField(_("Program Description"), max_length=765, null=True, blank=True)
    sector = models.ManyToManyField(Sector, blank=True, verbose_name=_("Sector"))
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    budget_check = models.BooleanField(_("Enable Approval Authority"), default=False)
    country = models.ManyToManyField(Country, verbose_name=_("Country"))
    user_access = models.ManyToManyField(TolaUser, blank=True)
    public_dashboard = models.BooleanField(_("Enable Public Dashboard"), default=False)

    class Meta:
        verbose_name=_("Program")
        ordering = ('name',)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if not 'force_insert' in kwargs:
            kwargs['force_insert'] = False
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Program, self).save()

    @property
    def countries(self):
        return ', '.join([x.country for x in self.country.all()])

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class ApprovalAuthority(models.Model):
    approval_user = models.ForeignKey(TolaUser,help_text=_('User with Approval Authority'), blank=True, null=True, related_name="auth_approving", verbose_name=_("Tola User"))
    budget_limit = models.IntegerField(null=True, blank=True)
    fund = models.CharField(_("Fund"),max_length=255,null=True, blank=True)
    country = models.ForeignKey("Country", null=True, blank=True, verbose_name=_("Country"))
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('approval_user',)
        verbose_name_plural = _("Tola Approval Authority")

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(ApprovalAuthority, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.approval_user.user.first_name + " " + self.approval_user.user.last_name


class Province(models.Model):
    name = models.CharField(_("Admin Level 1"), max_length=255, blank=True)
    country = models.ForeignKey(Country, verbose_name=_("Country"))
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _("Admin Level 1")
        verbose_name_plural = _("Admin Level 1")

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Province, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'create_date')
    search_fields = ('name','country__country')
    list_filter = ('create_date','country')
    display = 'Admin Level 1'


class District(models.Model):
    name = models.CharField(_("Admin Level 2"), max_length=255, blank=True)
    province = models.ForeignKey(Province,verbose_name=_("Admin Level 1"))
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _("Admin Level 2")
        verbose_name_plural = _("Admin Level 2")

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(District, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'create_date')
    search_fields = ('create_date','province')
    list_filter = ('province__country__country','province')
    display = 'Admin Level 2'


class AdminLevelThree(models.Model):
    name = models.CharField(_("Admin Level 3"), max_length=255, blank=True)
    district = models.ForeignKey(District,verbose_name=_("Admin Level 2"))
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _("Admin Level 3")
        verbose_name_plural = _("Admin Level 3")

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(AdminLevelThree, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class AdminLevelThreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'create_date')
    search_fields = ('name','district__name')
    list_filter = ('district__province__country__country','district')
    display = 'Admin Level 3'


class Village(models.Model):
    name = models.CharField(_("Admin Level 4"), max_length=255, blank=True)
    district = models.ForeignKey(District,null=True,blank=True, verbose_name=_("District"))
    admin_3 = models.ForeignKey(AdminLevelThree,verbose_name=_("Admin Level 3"),null=True,blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = _("Admin Level 4")
        verbose_name_plural = _("Admin Level 4")

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Village, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class VillageAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'create_date', 'edit_date')
    list_filter = ('district__province__country__country','district')
    display = 'Admin Level 4'

class Office(models.Model):
    name = models.CharField(_("Office Name"), max_length=255, blank=True)
    code = models.CharField(_("Office Code"), max_length=255, blank=True)
    province = models.ForeignKey(Province,verbose_name=_("Admin Level 1"))
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name=_("Office")
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


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'province', 'create_date', 'edit_date')
    search_fields = ('name','province__name','code')
    list_filter = ('create_date','province__country__country')
    display = 'Office'


class ProfileType(models.Model):
    profile = models.CharField(_("Profile Type"), max_length=255, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name=_("Profile Type")
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


class ProfileTypeAdmin(admin.ModelAdmin):
    list_display = ('profile', 'create_date', 'edit_date')
    display = 'ProfileType'


# Add land classification - 'Rural', 'Urban', 'Peri-Urban', tola-help issue #162
class LandType(models.Model):
    classify_land = models.CharField(_("Land Classification"), help_text=_("Rural, Urban, Peri-Urban"), max_length=100, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name=_("Land Type")
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


class LandTypeAdmin(admin.ModelAdmin):
    list_display = ('classify_land', 'create_date', 'edit_date')
    display = 'Land Type'


class SiteProfileManager(models.Manager):
    def get_queryset(self):
        return super(SiteProfileManager, self).get_queryset().prefetch_related().select_related('country','province','district','admin_level_three','type')


class SiteProfile(models.Model):
    profile_key = models.UUIDField(default=uuid.uuid4, unique=True),
    name = models.CharField(_("Site Name"), max_length=255, blank=False)
    type = models.ForeignKey(ProfileType, blank=True, null=True, verbose_name=_("Type"))
    office = models.ForeignKey(Office, blank=True, null=True, verbose_name=_("Office"))
    contact_leader = models.CharField(_("Contact Name"), max_length=255, blank=True, null=True)
    date_of_firstcontact = models.DateTimeField(_("Date of First Contact"), null=True, blank=True)
    contact_number = models.CharField(_("Contact Number"), max_length=255, blank=True, null=True)
    num_members = models.CharField(_("Number of Members"), max_length=255, blank=True, null=True)
    info_source = models.CharField(_("Data Source"),max_length=255, blank=True, null=True)
    total_num_households = models.IntegerField(_("Total # Households"), help_text="", null=True, blank=True)
    avg_household_size = models.DecimalField(_("Average Household Size"), decimal_places=14,max_digits=25, default=Decimal("0.00"))
    male_0_5 = models.IntegerField(_("Male age 0-5"), null=True, blank=True)
    female_0_5 = models.IntegerField(_("Female age 0-5"), null=True, blank=True)
    male_6_9 = models.IntegerField(_("Male age 6-9"), null=True, blank=True)
    female_6_9 = models.IntegerField(_("Female age 6-9"), null=True, blank=True)
    male_10_14 = models.IntegerField(_("Male age 10-14"), null=True, blank=True)
    female_10_14 = models.IntegerField(_("Female age 10-14"), null=True, blank=True)
    male_15_19 = models.IntegerField(_("Male age 15-19"), null=True, blank=True)
    female_15_19 = models.IntegerField(_("Female age 15-19"), null=True, blank=True)
    male_20_24 = models.IntegerField(_("Male age 20-24"), null=True, blank=True)
    female_20_24 = models.IntegerField(_("Female age 20-24"), null=True, blank=True)
    male_25_34 = models.IntegerField(_("Male age 25-34"), null=True, blank=True)
    female_25_34 = models.IntegerField(_("Female age 25-34"), null=True, blank=True)
    male_35_49 = models.IntegerField(_("Male age 35-49"), null=True, blank=True)
    female_35_49 = models.IntegerField(_("Female age 35-49"), null=True, blank=True)
    male_over_50 = models.IntegerField(_("Male Over 50"), null=True, blank=True)
    female_over_50 = models.IntegerField(_("Female Over 50"), null=True, blank=True)
    total_population = models.IntegerField(null=True, blank=True, verbose_name=_("Total population"))
    total_male = models.IntegerField(null=True, blank=True, verbose_name=_("Total male"))
    total_female = models.IntegerField(null=True, blank=True, verbose_name=_("Total female"))
    classify_land = models.ForeignKey(LandType, blank=True, null=True, verbose_name=_("Classify land"))
    total_land = models.IntegerField(_("Total Land"), help_text="In hectares/jeribs", null=True, blank=True)
    total_agricultural_land = models.IntegerField(_("Total Agricultural Land"), help_text="In hectares/jeribs", null=True, blank=True)
    total_rainfed_land = models.IntegerField(_("Total Rain-fed Land"), help_text="In hectares/jeribs", null=True, blank=True)
    total_horticultural_land = models.IntegerField(_("Total Horticultural Land"), help_text="In hectares/jeribs", null=True, blank=True)
    total_literate_peoples = models.IntegerField(_("Total Literate People"), help_text="", null=True, blank=True)
    literate_males = models.IntegerField(_("% of Literate Males"), help_text="%", null=True, blank=True)
    literate_females = models.IntegerField(_("% of Literate Females"), help_text="%", null=True, blank=True)
    literacy_rate = models.IntegerField(_("Literacy Rate (%)"), help_text="%", null=True, blank=True)
    populations_owning_land = models.IntegerField(_("Households Owning Land"), help_text="(%)", null=True, blank=True)
    avg_landholding_size = models.DecimalField(_("Average Landholding Size"), decimal_places=14,max_digits=25, help_text=_("In hectares/jeribs"), default=Decimal("0.00"))
    households_owning_livestock = models.IntegerField(_("Households Owning Livestock"), help_text="(%)", null=True, blank=True)
    animal_type = models.CharField(_("Animal Types"), help_text=_("List Animal Types"), max_length=255, null=True, blank=True)
    country = models.ForeignKey(Country, verbose_name=_("Country"))
    province = models.ForeignKey(Province, verbose_name=_("Administrative Level 1"), null=True, blank=True)
    district = models.ForeignKey(District, verbose_name=_("Administrative Level 2"), null=True, blank=True)
    admin_level_three = models.ForeignKey(AdminLevelThree, verbose_name=_("Administrative Level 3"), null=True, blank=True)
    village = models.CharField(_("Administrative Level 4"), help_text="", max_length=255, null=True, blank=True)
    latitude = models.DecimalField(_("Latitude (Decimal Coordinates)"), decimal_places=16,max_digits=25, default=Decimal("0.00"))
    longitude = models.DecimalField(_("Longitude (Decimal Coordinates)"), decimal_places=16,max_digits=25, default=Decimal("0.00"))
    status = models.BooleanField(_("Site Active"), default=True)
    approval = models.CharField(_("Approval"), default=_("in progress"), max_length=255, blank=True, null=True)
    approved_by = models.ForeignKey(TolaUser,help_text=_('This is the Provincial Line Manager'), blank=True, null=True, related_name="comm_approving", verbose_name=_("Approved by"))
    filled_by = models.ForeignKey(TolaUser, help_text=_('This is the originator'), blank=True, null=True, related_name="comm_estimate", verbose_name=_("Filled by"))
    location_verified_by = models.ForeignKey(TolaUser, help_text=_('This should be GIS Manager'), blank=True, null=True, related_name="comm_gis", verbose_name=_("Location verified by"))
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
            self.create_date = timezone.now()
            self.edit_date = timezone.now()

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


class Capacity(models.Model):
    capacity = models.CharField(_("Capacity"), max_length=255, blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('capacity',)
        verbose_name_plural = _("Capacity")

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Capacity, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.capacity


class CapacityAdmin(admin.ModelAdmin):
    list_display = ('capacity', 'create_date', 'edit_date')
    display = 'Capacity'


class StakeholderType(models.Model):
    name = models.CharField(_("Stakeholder Type"), max_length=255, blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = _("Stakeholder Types")

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(StakeholderType, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.name


class StakeholderTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'edit_date')
    display = 'Stakeholder Types'
    list_filter = ('create_date')
    search_fields = ('name')


class Evaluate(models.Model):
    evaluate = models.CharField(_("How will you evaluate the outcome or impact of the project?"), max_length=255, blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('evaluate',)
        verbose_name_plural = _("Evaluate")

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Evaluate, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.evaluate


class EvaluateAdmin(admin.ModelAdmin):
    list_display = ('evaluate', 'create_date', 'edit_date')
    display = 'Evaluate'


class ProjectType(models.Model):
    name = models.CharField(_("Type of Activity"), max_length=135)
    description = models.CharField(_("Description"), max_length=765)
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
        verbose_name=_("Project Type")
        ordering = ('name',)


class ProjectTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'create_date', 'edit_date')
    display = 'Project Type'


class Template(models.Model):
    name = models.CharField(_("Name of Document"), max_length=135)
    documentation_type = models.CharField(_("Type (File or URL)"), max_length=135)
    description = models.CharField(_("Description"), max_length=765)
    file_field = models.FileField(upload_to="uploads", blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Template, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name=_("Template")
        ordering = ('name',)


class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'documentation_type', 'file_field', 'create_date', 'edit_date')
    display = 'Template'


class StakeholderManager(models.Manager):
    def get_queryset(self):
        return super(StakeholderManager, self).get_queryset().prefetch_related('contact', 'sectors').select_related('country','type','formal_relationship_document','vetting_document')


class Stakeholder(models.Model):
    name = models.CharField(_("Stakeholder/Organization Name"), max_length=255, blank=True, null=True)
    type = models.ForeignKey(StakeholderType, blank=True, null=True, verbose_name=_("Type"))
    contact = models.ManyToManyField(Contact, max_length=255, blank=True, verbose_name=_("Contact"))
    country = models.ForeignKey(Country, verbose_name=_("Country"))
    #sector = models.ForeignKey(Sector, blank=True, null=True, related_name='sects')
    sectors = models.ManyToManyField(Sector, blank=True, verbose_name=_("Sectors"))
    stakeholder_register = models.BooleanField(_("Has this partner been added to stakeholder register?"))
    formal_relationship_document = models.ForeignKey('Documentation', verbose_name=_("Formal Written Description of Relationship"), null=True, blank=True, related_name="relationship_document")
    vetting_document = models.ForeignKey('Documentation', verbose_name=_("Vetting/ due diligence statement"), null=True, blank=True, related_name="vetting_document")
    approval = models.CharField(_("Approval"), default="in progress", max_length=255, blank=True, null=True)
    approved_by = models.ForeignKey(TolaUser, help_text='', blank=True, null=True, related_name="stake_approving", verbose_name=_("Approved by"))
    filled_by = models.ForeignKey(TolaUser, help_text='', blank=True, null=True, related_name="stake_filled", verbose_name=_("Filled by"))
    notes = models.TextField(_("Notes"), max_length=765, blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    #optimize query
    objects = StakeholderManager()

    class Meta:
        ordering = ('country','name','type')
        verbose_name_plural = _("Stakeholders")

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Stakeholder, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.name)


class StakeholderAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'country', 'create_date')
    display = 'Stakeholders'
    list_filter = ('country','type','sector')


class ProjectAgreementManager(models.Manager):
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
        return super(ProjectAgreementManager, self).get_queryset().select_related('office','approved_by','approval_submitted_by')

# Project Initiation, admin is handled in the admin.py
# TODO: Clean up unused fields and rename model with manual migration file
"""
https://docs.djangoproject.com/en/dev/ref/migration-operations/#renamemodel

class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0001_initial'),
    ]

    operations = [
        operations.RenameModel("ProjectAgreement", "WorkflowLevelOne")
    ]
"""
class ProjectAgreement(models.Model):
    agreement_key = models.UUIDField(default=uuid.uuid4, unique=True),
    short = models.BooleanField(default=True,verbose_name=_("Short Form (recommended)"))
    program = models.ForeignKey(Program, verbose_name=_("Program"), related_name="agreement")
    date_of_request = models.DateTimeField(_("Date of Request"), blank=True, null=True)
    # Rename to more generic "nonproject" names
    project_name = models.CharField(_("Project Name"), help_text=_('Please be specific in your name.  Consider that your Project Name includes WHO, WHAT, WHERE, HOW'), max_length=255)
    project_type = models.ForeignKey(ProjectType, verbose_name=_("Project Type"), help_text='', max_length=255, blank=True, null=True)
    project_activity = models.CharField(_("Project Activity"), help_text=_('This should come directly from the activities listed in the Logframe'), max_length=255, blank=True, null=True)
    project_description = models.TextField(_("Project Description"), help_text='', blank=True, null=True)
    site = models.ManyToManyField(SiteProfile, blank=True)
    has_rej_letter = models.BooleanField(_("If Rejected: Rejection Letter Sent?"), help_text=_('If yes attach copy'), default=False)
    activity_code = models.CharField(_("Project Code"), help_text='', max_length=255, blank=True, null=True)
    office = models.ForeignKey(Office, verbose_name=_("Office"), null=True, blank=True)
    cod_num = models.CharField(_("Project COD #"), max_length=255, blank=True, null=True)
    sector = models.ForeignKey("Sector", verbose_name=_("Sector"), blank=True, null=True)
    project_design = models.CharField(_("Activity design for"), max_length=255, blank=True, null=True)
    account_code = models.CharField(_("Fund Code"), help_text='', max_length=255, blank=True, null=True)
    lin_code = models.CharField(_("LIN Code"), help_text='', max_length=255, blank=True, null=True)
    staff_responsible = models.CharField(_("Staff Responsible"), max_length=255, blank=True, null=True)
    partners = models.BooleanField(_("Are there partners involved?"), default=0)
    name_of_partners = models.CharField(_("Name of Partners"), max_length=255, blank=True, null=True)
    stakeholder = models.ManyToManyField(Stakeholder,verbose_name=_("Stakeholders"), blank=True)
    effect_or_impact = models.TextField(_("What is the anticipated Outcome or Goal?"), blank=True, null=True)
    expected_start_date = models.DateTimeField(_("Expected starting date"), blank=True, null=True)
    expected_end_date = models.DateTimeField(_("Expected ending date"),blank=True, null=True)
    expected_duration = models.CharField(_("Expected duration"), help_text=_("[MONTHS]/[DAYS]"), blank=True, null=True, max_length=255)
    beneficiary_type = models.CharField(_("Type of direct beneficiaries"), help_text=_("i.e. Farmer, Association, Student, Govt, etc."), max_length=255, blank=True, null=True)
    estimated_num_direct_beneficiaries = models.CharField(_("Estimated number of direct beneficiaries"), help_text=_("Please provide achievable estimates as we will use these as our 'Targets'"),max_length=255, blank=True, null=True)
    average_household_size = models.CharField(_("Average Household Size"), help_text=_("Refer to Form 01 - Community Profile"),max_length=255, blank=True, null=True)
    estimated_num_indirect_beneficiaries = models.CharField(_("Estimated Number of indirect beneficiaries"), help_text=_("This is a calculation - multiply direct beneficiaries by average household size"),max_length=255, blank=True, null=True)
    total_estimated_budget = models.DecimalField(_("Total Project Budget"), decimal_places=2,max_digits=12, help_text=_("In USD"), default=Decimal("0.00"),blank=True)
    mc_estimated_budget = models.DecimalField(_("Organizations portion of Project Budget"), decimal_places=2,max_digits=12, help_text=_("In USD"), default=Decimal("0.00"),blank=True)
    local_total_estimated_budget = models.DecimalField(_("Estimated Total in Local Currency"), decimal_places=2,max_digits=12, help_text=_("In Local Currency"), default=Decimal("0.00"),blank=True)
    local_mc_estimated_budget = models.DecimalField(_("Estimated Organization Total in Local Currency"), decimal_places=2,max_digits=12, help_text=_("Total portion of estimate for your agency"), default=Decimal("0.00"),blank=True)
    exchange_rate = models.CharField(help_text=_("Local Currency exchange rate to USD"), max_length=255, blank=True, null=True)
    exchange_rate_date = models.DateField(help_text=_("Date of exchange rate"), blank=True, null=True)
    """
    Start Clean Up - These can be removed
    """
    community_rep = models.CharField(_("Community Representative"), max_length=255, blank=True, null=True)
    community_rep_contact = models.CharField(_("Community Representative Contact"), help_text='Can have mulitple contact numbers', max_length=255, blank=True, null=True)
    community_mobilizer = models.CharField(_("Community Mobilizer"), max_length=255, blank=True, null=True)
    community_mobilizer_contact = models.CharField(_("Community Mobilizer Contact Number"), max_length=255, blank=True, null=True)
    community_proposal = models.FileField(_("Community Proposal"), upload_to='uploads', blank=True, null=True)
    estimate_male_trained = models.IntegerField(_("Estimated # of Male Trained"),blank=True,null=True)
    estimate_female_trained = models.IntegerField(_("Estimated # of Female Trained"),blank=True,null=True)
    estimate_total_trained = models.IntegerField(_("Estimated Total # Trained"),blank=True,null=True)
    estimate_trainings = models.IntegerField(_("Estimated # of Trainings Conducted"),blank=True,null=True)
    distribution_type = models.CharField(_("Type of Items Distributed"),max_length=255,null=True,blank=True)
    distribution_uom = models.CharField(_("Unit of Measure"),max_length=255,null=True,blank=True)
    distribution_estimate = models.CharField(_("Estimated # of Items Distributed"),max_length=255,null=True,blank=True)
    cfw_estimate_male = models.IntegerField(_("Estimated # of Male Laborers"),blank=True,null=True)
    cfw_estimate_female = models.IntegerField(_("Estimated # of Female Laborers"),blank=True,null=True)
    cfw_estimate_total = models.IntegerField(_("Estimated Total # of Laborers"),blank=True,null=True)
    cfw_estimate_project_days = models.IntegerField(_("Estimated # of Project Days"),blank=True,null=True)
    cfw_estimate_person_days = models.IntegerField(_("Estimated # of Person Days"),blank=True,null=True)
    cfw_estimate_cost_materials = models.CharField(_("Estimated Total Cost of Materials"),max_length=255,blank=True,null=True)
    cfw_estimate_wages_budgeted= models.CharField(_("Estimated Wages Budgeted"),max_length=255,blank=True,null=True)
    """
    End Clean Up
    """
    estimation_date = models.DateTimeField(_("Estimation date"), blank=True, null=True)
    estimated_by = models.ForeignKey(TolaUser, blank=True, null=True,verbose_name="Originated By", related_name="estimating")
    estimated_by_date = models.DateTimeField("Date Originated", null=True, blank=True)
    checked_by = models.ForeignKey(TolaUser, blank=True, null=True, related_name="checking",verbose_name=_("Checked by"))
    checked_by_date = models.DateTimeField("Date Checked", null=True, blank=True)
    reviewed_by = models.ForeignKey(TolaUser, verbose_name="Request review", blank=True, null=True, related_name="reviewing" )
    reviewed_by_date = models.DateTimeField("Date Verified", null=True, blank=True)
    finance_reviewed_by = models.ForeignKey(TolaUser, blank=True, null=True, related_name="finance_reviewing", verbose_name=_("Finance reviewed by"))
    finance_reviewed_by_date = models.DateTimeField(_("Date Reviewed by Finance"), null=True, blank=True)
    me_reviewed_by = models.ForeignKey(TolaUser, blank=True, null=True, verbose_name=_("M&E Reviewed by"), related_name="reviewing_me")
    me_reviewed_by_date = models.DateTimeField(_("Date Reviewed by M&E"), null=True, blank=True)
    capacity = models.ManyToManyField(Capacity,verbose_name=_("Sustainability Plan"), blank=True)
    evaluate = models.ManyToManyField(Evaluate, blank=True, verbose_name=_("Evaluate"))
    approval = models.CharField(_("Approval Status"), default="in progress", max_length=255, blank=True, null=True)
    approved_by = models.ForeignKey(TolaUser, blank=True, null=True, related_name="approving_agreement", verbose_name="Request approval")
    approved_by_date = models.DateTimeField(_("Date Approved"), null=True, blank=True)
    approval_submitted_by = models.ForeignKey(TolaUser, blank=True, null=True, related_name="submitted_by_agreement", verbose_name=_("Approval submitted by"))
    approval_remarks = models.CharField(_("Approval Remarks"), max_length=255, blank=True, null=True)
    justification_background = models.TextField(_("General Background and Problem Statement"), blank=True, null=True)
    risks_assumptions = models.TextField(_("Risks and Assumptions"), blank=True, null=True)
    justification_description_community_selection = models.TextField(_("Description of Stakeholder Selection Criteria"), blank=True, null=True)
    description_of_project_activities = models.TextField(_("Description of project activities"), blank=True, null=True)
    description_of_government_involvement = models.TextField(_("Description of government involvement"),blank=True, null=True)
    description_of_community_involvement = models.TextField(_("Description of community involvement"), blank=True, null=True)
    community_project_description = models.TextField(_("Describe the project you would like the program to consider"), blank=True, null=True, help_text="Description must describe how the Community Proposal meets the project criteria")
    create_date = models.DateTimeField(_("Date Created"), null=True, blank=True)
    edit_date = models.DateTimeField(_("Last Edit Date"), null=True, blank=True)
    history = HistoricalRecords()
    #optimize base query for all classbasedviews
    objects = ProjectAgreementManager()

    class Meta:
        ordering = ('project_name',)
        verbose_name_plural = _("Project Initiation")
        permissions = (
            ("can_approve", "Can approve initiation"),
        )

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        # defaults don't work if they aren't in the form so preset these to 0
        if self.total_estimated_budget == None:
            self.total_estimated_budget = Decimal("0.00")
        if self.mc_estimated_budget == None:
            self.mc_estimated_budget = Decimal("0.00")
        if self.local_total_estimated_budget == None:
            self.local_total_estimated_budget = Decimal("0.00")
        if self.local_mc_estimated_budget == None:
            self.local_mc_estimated_budget = Decimal("0.00")

        self.edit_date = timezone.now()
        super(ProjectAgreement, self).save()

    @property
    def project_name_clean(self):
        return self.project_name.encode('ascii', 'ignore')

    @property
    def sites(self):
        return ', '.join([x.name for x in self.site.all()])

    @property
    def stakeholders(self):
        return ', '.join([x.name for x in self.stakeholder.all()])

    @property
    def capacities(self):
        return ', '.join([x.capacity for x in self.capacity.all()])

    @property
    def evaluations(self):
        return ', '.join([x.evaluate for x in self.evaluate.all()])

    # displayed in admin templates
    def __unicode__(self):
        new_name = unicode(self.office) + unicode(" - ") + unicode(self.project_name)
        return new_name

# Project Tracking, admin is handled in the admin.py
# TODO: Clean up unused fields and rename model with manual migration file
"""
https://docs.djangoproject.com/en/dev/ref/migration-operations/#renamemodel

class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0001_initial'),
    ]

    operations = [
        operations.RenameModel("ProjectComplete", "WorkflowLevelTwo")
    ]
"""
class ProjectComplete(models.Model):
    short = models.BooleanField(default=True,verbose_name="Short Form (recommended)")
    program = models.ForeignKey(Program, null=True, blank=True, related_name="complete", verbose_name=_("Program"))
    project_agreement = models.OneToOneField(ProjectAgreement, verbose_name=_("Project Initiation"))
    # Rename to more generic "nonproject" names
    activity_code = models.CharField(_("Project Code"), max_length=255, blank=True, null=True)
    project_name = models.CharField(_("Project Name"), max_length=255, blank=True, null=True)
    project_activity = models.CharField(_("Project Activity"), max_length=255, blank=True, null=True)
    project_type = models.ForeignKey(ProjectType, max_length=255, blank=True, null=True, verbose_name=_("Project Type"))
    office = models.ForeignKey(Office, null=True, blank=True, verbose_name=_("Office"))
    sector = models.ForeignKey("Sector", blank=True, null=True, verbose_name=_("Sector"))
    expected_start_date = models.DateTimeField(_("Expected start date"), help_text=_("Imported from Project Initiation"), blank=True, null=True)
    expected_end_date = models.DateTimeField(_("Expected end date"), help_text=_("Imported Project Initiation"), blank=True, null=True)
    expected_duration = models.CharField(_("Expected Duration"), max_length=255, help_text=_("Imported from Project Initiation"), blank=True, null=True)
    actual_start_date = models.DateTimeField(_("Actual start date"), help_text=_("Imported from Project Initiation"), blank=True, null=True)
    actual_end_date = models.DateTimeField(_("Actual end date"), blank=True, null=True)
    actual_duration = models.CharField(_("Actual duaration"), max_length=255, blank=True, null=True)
    on_time = models.BooleanField(default=None)
    stakeholder = models.ManyToManyField(Stakeholder, blank=True, verbose_name=_("Stakeholder"))
    no_explanation = models.TextField(_("If not on time explain delay"), blank=True, null=True)
    account_code = models.CharField(_("Fund Code"), help_text='', max_length=255, blank=True, null=True)
    lin_code = models.CharField(_("LIN Code"), help_text='', max_length=255, blank=True, null=True)
    estimated_budget = models.DecimalField(_("Estimated Budget"), decimal_places=2,max_digits=12,help_text="", default=Decimal("0.00") ,blank=True)
    actual_budget = models.DecimalField(_("Actual Cost"), decimal_places=2,max_digits=20, default=Decimal("0.00"), blank=True, help_text="What was the actual final cost?  This should match any financial documentation you have in the file.   It should be completely documented and verifiable by finance and any potential audit")
    actual_cost_date = models.DateTimeField(_("Actual cost date"), blank=True, null=True)
    budget_variance = models.CharField(_("Budget versus Actual variance"), blank=True, null=True, max_length=255)
    explanation_of_variance = models.CharField(_("Explanation of variance"), blank=True, null=True, max_length=255)
    total_cost = models.DecimalField(_("Estimated Budget for Organization"),decimal_places=2,max_digits=12,help_text="In USD", default=Decimal("0.00"),blank=True)
    agency_cost = models.DecimalField(_("Actual Cost for Organization"), decimal_places=2,max_digits=12,help_text="In USD", default=Decimal("0.00"),blank=True)
    local_total_cost = models.DecimalField(_("Actual Cost"), decimal_places=2,max_digits=12, help_text="In Local Currency", default=Decimal("0.00"),blank=True)
    local_agency_cost = models.DecimalField(_("Actual Cost for Organization"), decimal_places=2,max_digits=12, help_text="In Local Currency", default=Decimal("0.00"),blank=True)
    exchange_rate = models.CharField(help_text=_("Local Currency exchange rate to USD"), max_length=255, blank=True, null=True)
    exchange_rate_date = models.DateField(help_text=_("Date of exchange rate"), blank=True, null=True)
    """
    Start Clean Up - These can be removed
    """
    beneficiary_type = models.CharField(_("Type of direct beneficiaries"), help_text=_("i.e. Farmer, Association, Student, Govt, etc."), max_length=255, blank=True, null=True)
    average_household_size = models.CharField(_("Average Household Size"), help_text=_("Refer to Form 01 - Community Profile"),max_length=255, blank=True, null=True)
    indirect_beneficiaries = models.CharField(_("Estimated Number of indirect beneficiaries"), help_text=_("This is a calculation - multiply direct beneficiaries by average household size"),max_length=255, blank=True, null=True)
    direct_beneficiaries = models.CharField(_("Actual Direct Beneficiaries"), max_length=255, blank=True, null=True)
    jobs_created = models.CharField(_("Number of Jobs Created"), max_length=255, blank=True, null=True)
    jobs_part_time = models.CharField(_("Part Time Jobs"), max_length=255, blank=True, null=True)
    jobs_full_time = models.CharField(_("Full Time Jobs"), max_length=255, blank=True, null=True)
    progress_against_targets = models.IntegerField(_("Progress against Targets (%)"),blank=True,null=True)
    government_involvement = models.CharField(_("Government Involvement"), max_length=255, blank=True, null=True)
    community_involvement = models.CharField(_("Community Involvement"), max_length=255, blank=True, null=True)
    """
    End Clean Up
    """
    community_handover = models.BooleanField(_("CommunityHandover/Sustainability Maintenance Plan"), help_text=_('Check box if it was completed'), default=None)
    capacity_built = models.TextField(_("Describe how sustainability was ensured for this project?"), max_length=755, blank=True, null=True)
    quality_assured = models.TextField(_("How was quality assured for this project"), max_length=755, blank=True, null=True)
    issues_and_challenges = models.TextField("List any issues or challenges faced (include reasons for delays)", blank=True, null=True)
    lessons_learned= models.TextField(_("Lessons learned"), blank=True, null=True)
    site = models.ManyToManyField(SiteProfile, blank=True, verbose_name=_("Site"))
    estimated_by = models.ForeignKey(TolaUser, blank=True, null=True, related_name="estimating_complete", verbose_name=_("Estimated by"))
    checked_by = models.ForeignKey(TolaUser, blank=True, null=True, related_name="checking_complete", verbose_name=_("Checked by"))
    reviewed_by = models.ForeignKey(TolaUser, blank=True, null=True, related_name="reviewing_complete", verbose_name=_("Reviewed by"))
    approval = models.CharField(_("Approval Status"), default="in progress", max_length=255, blank=True, null=True)
    approved_by = models.ForeignKey(TolaUser, blank=True, null=True, related_name="approving_agreement_complete", verbose_name=_("Approved by"))
    approval_submitted_by = models.ForeignKey(TolaUser, blank=True, null=True, related_name="submitted_by_complete", verbose_name=_("Approval submitted by"))
    approval_remarks = models.CharField(_("Approval Remarks"), max_length=255, blank=True, null=True)
    create_date = models.DateTimeField(_("Date Created"), null=True, blank=True)
    edit_date = models.DateTimeField(_("Last Edit Date"), null=True, blank=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ('project_name',)
        verbose_name_plural = _("Project Tracking")

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        # defaults don't work if they aren't in the form so preset these to 0
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
        self.edit_date = timezone.now()
        super(ProjectComplete, self).save()

    # displayed in admin templates
    def __unicode__(self):
        new_name = unicode(self.office) + unicode(" - ") + unicode(self.project_name)
        return new_name

    @property
    def project_name_clean(self):
        return self.project_name.encode('ascii', 'ignore')


# Project Documents, admin is handled in the admin.py
class Documentation(models.Model):
    name = models.CharField(_("Name of Document"), max_length=135, blank=True, null=True)
    url = models.CharField(_("URL (Link to document or document repository)"), blank=True, null=True, max_length=135)
    description = models.CharField(_("Description"), max_length=255, blank=True, null=True)
    template = models.ForeignKey(Template, blank=True, null=True, verbose_name=_("Template"))
    file_field = models.FileField(upload_to="uploads", blank=True, null=True)
    project = models.ForeignKey(ProjectAgreement, blank=True, null=True, verbose_name=_("Project"))
    program = models.ForeignKey(Program, verbose_name=_("Program"))
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

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
        verbose_name_plural = _("Documentation")


# TODO: Rename model with manual migration file
"""
https://docs.djangoproject.com/en/dev/ref/migration-operations/#renamemodel

class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0001_initial'),
    ]

    operations = [
        operations.RenameModel("Benchmarks", "WorkflowLevelThree")
    ]
"""
class Benchmarks(models.Model):
    percent_complete = models.IntegerField(_("% complete"), blank=True, null=True)
    percent_cumulative = models.IntegerField(_("% cumulative completion"), blank=True, null=True)
    est_start_date = models.DateTimeField(_("Est start date"), null=True, blank=True)
    est_end_date = models.DateTimeField(_("Est end date"), null=True, blank=True)
    actual_start_date = models.DateTimeField(_("Actual start date"), null=True, blank=True)
    actual_end_date = models.DateTimeField(_("Actual end date"), null=True, blank=True)
    site = models.ForeignKey(SiteProfile, null=True, blank=True, verbose_name=_("site"))
    budget = models.IntegerField(_("Estimated Budget"), blank=True, null=True)
    cost = models.IntegerField(_("Actual Cost"), blank=True, null=True)
    description = models.CharField(_("Description"), max_length=255, blank=True)
    agreement = models.ForeignKey(ProjectAgreement,blank=True, null=True, verbose_name=_("Project Initiation"))
    complete = models.ForeignKey(ProjectComplete,blank=True, null=True, verbose_name=_("Complete"))
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('description',)
        verbose_name_plural = _("Project Components")

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Benchmarks, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.description


class BenchmarksAdmin(admin.ModelAdmin):
    list_display = ('description', 'agreement__name', 'create_date', 'edit_date')
    display = 'Project Components'


# TODO Delete not in use
class Monitor(models.Model):
    responsible_person = models.CharField(_("Person Responsible"), max_length=25, blank=True, null=True)
    frequency = models.CharField(_("Frequency"), max_length=25, blank=True, null=True)
    type = models.TextField(_("Type"), null=True, blank=True)
    agreement = models.ForeignKey(ProjectAgreement,blank=True, null=True, verbose_name=_("Project Initiation"))
    complete = models.ForeignKey(ProjectComplete,blank=True, null=True, verbose_name=_("complete"))
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('type',)
        verbose_name_plural = _("Monitors")

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Monitor, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return self.responsible_person


class MonitorAdmin(admin.ModelAdmin):
    list_display = ('responsible_person', 'frequency', 'type', 'create_date', 'edit_date')
    display = 'Monitor'


class Budget(models.Model):
    contributor = models.CharField(_("Contributor"), max_length=135, blank=True, null=True)
    description_of_contribution = models.CharField(_("Description of contribution"), max_length=255, blank=True, null=True)
    proposed_value = models.IntegerField(_("Value"),default=0, blank=True, null=True)
    agreement = models.ForeignKey(ProjectAgreement, blank=True, null=True, verbose_name=_("Project Initiation"))
    complete = models.ForeignKey(ProjectComplete, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_("Complete"))
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords()
    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Budget, self).save()

    def __unicode__(self):
        return self.contributor

    class Meta:
        ordering = ('contributor',)


class BudgetAdmin(admin.ModelAdmin):
    list_display = ('contributor', 'description_of_contribution', 'proposed_value', 'create_date', 'edit_date')
    display = 'Budget'


class Checklist(models.Model):
    name = models.CharField(_("Name"), max_length=255, null=True, blank=True,default="Checklist")
    agreement = models.ForeignKey(ProjectAgreement, null=True, blank=True, verbose_name=_("Project Initiation"))
    country = models.ForeignKey(Country,null=True,blank=True, verbose_name=_("Country"))
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('agreement',)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Checklist, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.agreement)


class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('name','country')
    list_filter = ('country','agreement')


class ChecklistItem(models.Model):
    item = models.CharField(_("Item"), max_length=255)
    checklist = models.ForeignKey(Checklist, verbose_name=_("Checklist"))
    in_file = models.BooleanField(default=False)
    not_applicable = models.BooleanField(default=False)
    global_item = models.BooleanField(default=False)
    owner = models.ForeignKey(TolaUser, null=True, blank=True, verbose_name=_("Owner"))
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name=_("Checklist Item")
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


class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('item','checklist','in_file')
    list_filter = ('checklist','global_item')


#Logged users
from django.contrib.auth.signals import user_logged_in, user_logged_out
from urllib2 import urlopen
import json


class LoggedUser(models.Model):
    # TODO: Tis does not seem to be used anywhere; perhaps it should be deelted
    username = models.CharField(_("Username"), max_length=30, primary_key=True)
    country = models.CharField(_("Country"), max_length=100, blank=False)
    email = models.CharField(_("Email"), max_length=100, blank=False, default='user@mercycorps.com')

    def __unicode__(self):
        return self.username

    def login_user(sender, request, user, **kwargs):
        print("login_user...........%s............................" % user )
        country = get_user_country(request)
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())

        user_id_list = []
        logged_user_id = request.user.id

        try:
            for session in active_sessions:
                data = session.get_decoded()

                user_id_list.append(data.get('_auth_user_id', None))

                if logged_user_id in user_id_list:
                    LoggedUser(username=user.username, country=country, email=user.email).save()

                if data.get('google-oauth2_state'):
                    LoggedUser(username=user.username, country=country, email=user.email).save()

        except Exception, e:
            pass



    def logout_user(sender, request, user, **kwargs):
        print("logout_user...........%s............................" % user )
        try:
            user = LoggedUser.objects.get(pk=user.username)
            user.delete()

        except LoggedUser.DoesNotExist:
            pass

    # user_logged_in.connect(login_user)
    # user_logged_out.connect(logout_user)


def get_user_country(request):

    # Automatically geolocate the connecting IP
    ip = request.META.get('REMOTE_ADDR')
    try:
        response = urlopen('http://ipinfo.io/'+ip+'/json').read()
        response = json.loads(response)
        return response['country'].lower()

    except Exception, e:
        response = "undefined"
        return response



