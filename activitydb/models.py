from __future__ import unicode_literals

from django.db import models
from django.contrib import admin
from django.conf import settings
from datetime import datetime


class Country(models.Model):
    country = models.CharField("Country Name", max_length=255, blank=True)
    code = models.CharField("2 Letter Country Code", max_length=4, blank=True)
    description = models.CharField("Description/Notes", max_length=255, blank=True)
    latitude = models.CharField("Latitude", max_length=255, null=True, blank=True)
    longitude = models.CharField("Longitude", max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('country',)
        verbose_name_plural = "Countries"
        app_label = 'activitydb'

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Country, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.country


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'create_date', 'edit_date')
    display = 'Country'


class Sector(models.Model):
    sector = models.CharField("Sector Name", max_length=255, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('sector',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Sector, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.sector


class SectorAdmin(admin.ModelAdmin):
    list_display = ('sector', 'create_date', 'edit_date')
    display = 'Sector'


class Program(models.Model):
    gaitid = models.CharField("GAITID", max_length=255, blank=True, unique=True)
    name = models.CharField("Program Name", max_length=255, blank=True)
    funding_status = models.CharField("Funding Status", max_length=255, blank=True)
    cost_center = models.CharField("Fund Code", max_length=255, blank=True, null=True)
    description = models.CharField("Program Description", max_length=765, null=True, blank=True)
    sector = models.ForeignKey(Sector, null=True,blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    country = models.ManyToManyField(Country)

    class Meta:
        ordering = ('create_date',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if not 'force_insert' in kwargs:
            kwargs['force_insert'] = False
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Program, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.name


class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'create_date', 'edit_date')
    display = 'Program'


class ApprovalAuthority(models.Model):
    approval_user = models.ForeignKey(settings.AUTH_USER_MODEL,help_text='User with Approval Authority', blank=True, null=True, related_name="auth_approving")
    budget_limit = models.IntegerField(null=True, blank=True)
    fund = models.IntegerField("Fund",null=True, blank=True)
    country = models.ForeignKey("Country", null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('approval_user',)
        verbose_name_plural = "Approval Authority"

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ApprovalAuthority, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.approval_user


class ApprovalAuthorityAdmin(admin.ModelAdmin):
    list_display = ('approval_user')
    display = 'Approval Authority'


class Province(models.Model):
    name = models.CharField("Province Name", max_length=255, blank=True)
    country = models.ForeignKey(Country)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Province, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.name


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'create_date', 'edit_date')
    display = 'Province'


class District(models.Model):
    name = models.CharField("District Name", max_length=255, blank=True)
    province = models.ForeignKey(Province)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(District, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.name


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'province', 'create_date', 'edit_date')
    display = 'District'


class Office(models.Model):
    name = models.CharField("Office Name", max_length=255, blank=True)
    code = models.CharField("Office Code", max_length=255, blank=True)
    province = models.ForeignKey(Province)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Office, self).save()

    #displayed in admin templates
    def __unicode__(self):
        new_name = unicode(self.name) + unicode(" - ") + unicode(self.code)
        return new_name


class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'province', 'create_date', 'edit_date')
    display = 'Office'


class Village(models.Model):
    name = models.CharField("Village Name", max_length=255, blank=True)
    district = models.ForeignKey(District)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Village, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.name


class VillageAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'create_date', 'edit_date')
    display = 'Village'


class ProfileType(models.Model):
    profile = models.CharField("Profile Type", max_length=255, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('profile',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ProfileType, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.profile


class SectorAdmin(admin.ModelAdmin):
    list_display = ('profile', 'create_date', 'edit_date')
    display = 'ProfileType'


class Community(models.Model):
    name = models.CharField("Profile Name", max_length=255, blank=True, null=True)
    type = models.ForeignKey(ProfileType, blank=True, null=True)
    office = models.ForeignKey(Office, default="1")
    existing_village = models.BooleanField("Is There an existing shura or CDC?", default="False")
    existing_village_descr = models.CharField("If Yes please describe", max_length=255, blank=True, null=True)
    community_leader = models.CharField("Community Malik/Elder Name", max_length=255, blank=True, null=True)
    head_of_institution = models.CharField("Head of Shura/Institution", max_length=255, blank=True, null=True)
    date_of_firstcontact = models.DateTimeField(null=True, blank=True)
    contact_number = models.CharField("Contact Number", max_length=255, blank=True, null=True)
    num_members = models.CharField("Number of Members", max_length=255, blank=True, null=True)
    distance_district_capital = models.IntegerField("Distance from District Capital", help_text="In KM", null=True, blank=True)
    distance_site_camp = models.IntegerField("Distance from Site Camp", help_text="In KM", null=True, blank=True)
    distance_field_office = models.IntegerField("Distance from MC Field Office", help_text="In KM", null=True, blank=True)
    total_num_households = models.IntegerField("Total # Households", help_text="", null=True, blank=True)
    avg_household_size = models.DecimalField("Average Household Size", decimal_places=14,max_digits=25, null=True, blank=True)
    male_0_14 = models.IntegerField("Male age 0-14", null=True, blank=True)
    female_0_14 = models.IntegerField("Female age 0-14", null=True, blank=True)
    male_15_24 = models.IntegerField("Male age 15-24 ", null=True, blank=True)
    female_15_24 = models.IntegerField("Female age 15-24", null=True, blank=True)
    male_25_59 = models.IntegerField("Male age 25-59", null=True, blank=True)
    female_25_59 = models.IntegerField("Female age 25-59", null=True, blank=True)
    male_over_60 = models.IntegerField("Male Over 60", null=True, blank=True)
    female_over_60 = models.IntegerField("Female Over 60", null=True, blank=True)
    total_population = models.IntegerField(null=True, blank=True)
    total_male = models.IntegerField(null=True, blank=True)
    total_female = models.IntegerField(null=True, blank=True)
    total_land = models.IntegerField("Total Land", help_text="In hectares/jeribs", null=True, blank=True)
    total_agricultural_land = models.IntegerField("Total Agricultural Land", help_text="In hectares/jeribs", null=True, blank=True)
    total_rainfed_land = models.IntegerField("Total Rain-fed Land", help_text="In hectares/jeribs", null=True, blank=True)
    total_horticultural_land = models.IntegerField("Total Horticultural Land", help_text="In hectares/jeribs", null=True, blank=True)
    total_literate_peoples = models.IntegerField("Total Literate People", help_text="", null=True, blank=True)
    literate_males = models.IntegerField("Number of Literate Males", help_text="", null=True, blank=True)
    literate_females = models.IntegerField("Number of Literate Females", help_text="", null=True, blank=True)
    literacy_rate = models.IntegerField("Literacy Rate (%)", help_text="", null=True, blank=True)
    population_owning_land = models.IntegerField("Population Owning Land", help_text="(%)", null=True, blank=True)
    avg_landholding_size = models.IntegerField("Average Landholding Size", help_text="In hectares/jeribs", null=True, blank=True)
    population_owning_livestock = models.IntegerField("Population Owning Livestock", help_text="(%)", null=True, blank=True)
    animal_type = models.CharField("Animal Types", help_text="List Animal Types", max_length=255, null=True, blank=True)
    country = models.ForeignKey(Country)
    province = models.ForeignKey(Province, null=True, blank=True)
    district = models.ForeignKey(District, null=True, blank=True)
    village = models.CharField("Village", help_text="", max_length=255, null=True, blank=True)
    latitude = models.DecimalField("Latitude (Decimal Coordinates)", decimal_places=14,max_digits=25, blank=True, null=True)
    longitude = models.DecimalField("Longitude (Decimal Coordinates)", decimal_places=14,max_digits=25, blank=True, null=True)
    altitude = models.DecimalField("Altitude (in meters)", decimal_places=14,max_digits=25, blank=True, null=True)
    precision = models.DecimalField("Precision (in meters)", decimal_places=14,max_digits=25, blank=True, null=True)
    approval = models.CharField("Approval", default="in progress", max_length=255, blank=True, null=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL,help_text='This is the Provincial Line Manager', blank=True, null=True, related_name="comm_approving")
    filled_by = models.ForeignKey(settings.AUTH_USER_MODEL, help_text='This is the originator', blank=True, null=True, related_name="comm_estimate")
    location_verified_by = models.ForeignKey(settings.AUTH_USER_MODEL, help_text='This should be GIS Manager', blank=True, null=True, related_name="comm_gis")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Communities"

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        self.code = str(self.country.code) + "-" + str(self.office.code) + "-" + str(self.name)
        super(Community, self).save()

    #displayed in admin templates
    def __unicode__(self):
        new_name = str(self.province) + " - " + str(self.name)
        return new_name


class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'code','office', 'country', 'district', 'province', 'village', 'cluster', 'longitude', 'latitude', 'create_date', 'edit_date')
    display = 'Community'


class Capacity(models.Model):
    capacity = models.CharField("Capacity", max_length=255, blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('capacity',)
        verbose_name_plural = "Capacity"

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Capacity, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.capacity


class CapacityAdmin(admin.ModelAdmin):
    list_display = ('capacity', 'create_date', 'edit_date')
    display = 'Capacity'


class Evaluate(models.Model):
    evaluate = models.CharField("How will you evaluate the outcome or impact of the project?", max_length=255, blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('evaluate',)
        verbose_name_plural = "Evaluate"

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Evaluate, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.evaluate


class EvaluateAdmin(admin.ModelAdmin):
    list_display = ('evaluate', 'create_date', 'edit_date')
    display = 'Evaluate'


class ProjectType(models.Model):
    name = models.CharField("Type of Activity", max_length=135)
    description = models.CharField(max_length=255)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    #onsave add create date or update edit date
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


class ProjectTypeOther(models.Model):
    name = models.CharField("Type of Activity", max_length=135)
    description = models.CharField(max_length=255)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ProjectTypeOther, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class ProjectTypeOtherAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'create_date', 'edit_date')
    display = 'Activity Type Other'


class Template(models.Model):
    name = models.CharField("Name of Document", max_length=135)
    documentation_type = models.CharField("Type (File or URL)", max_length=135)
    description = models.CharField(max_length=255)
    file_field = models.FileField(upload_to="uploads", blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    #onsave add create date or update edit date
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


class ProjectProposal(models.Model):
    program = models.ForeignKey(Program, null=True, blank=True, related_name="proposal")
    proposal_num = models.CharField("Proposal Number", max_length=255, blank=True, null=True)
    date_of_request = models.DateTimeField("Date of Request", null=True, blank=True)
    project_name = models.CharField("Activity Name", help_text='Please be specific in your name.  Consider that your Activity Name includes WHO, WHAT, WHERE, HOW', max_length=255)
    sector = models.ForeignKey(Sector, max_length=255, blank=True, null=True)
    project_type = models.ForeignKey(ProjectType, help_text='Please refer to Form 05 - Project Progress Summary', max_length=255, blank=True, null=True)
    project_activity = models.CharField("Project Activity", help_text='This should come directly from the activities listed in the Logframe', max_length=255, blank=True, null=True)
    office = models.ForeignKey(Office, null=True, blank=True)
    community = models.ManyToManyField(Community, blank=True)
    community_rep = models.CharField("Community Representative", max_length=255, blank=True, null=True)
    community_rep_contact = models.CharField("Community Representative Contact", help_text='Can have mulitple contact numbers', max_length=255, blank=True, null=True)
    community_mobilizer = models.CharField("MC Community Mobilizer", max_length=255, blank=True, null=True)
    community_mobilizer_contact = models.CharField("MC Community Mobilizer Contact Number", max_length=255, blank=True, null=True)
    has_rej_letter = models.BooleanField("If Rejected: Rejection Letter Sent?", help_text='If yes attach copy', default=False)
    rejection_letter = models.FileField("Rejection Letter", upload_to='uploads', blank=True, null=True)
    activity_code = models.CharField("Activity Code", help_text='If applicable at this stage, please request Activity Code from Kabul MEL', max_length=255, blank=True, null=True)
    project_description = models.TextField("Project Description", help_text='Description must meet the Criteria.  Will translate description into three languages: English, Dari and Pashto)', blank=True, null=True)
    approval = models.CharField("Status", default="in progress", max_length=255, blank=True, null=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL,help_text='This is the Provincial Line Manager', blank=True, null=True, related_name="approving")
    estimated_by = models.ForeignKey(settings.AUTH_USER_MODEL, help_text='This is the originator', blank=True, null=True, related_name="estimate")
    approval_submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="requesting")
    approval_remarks = models.CharField("Approval Remarks", max_length=255, blank=True, null=True)
    device_id = models.CharField("Device ID", max_length=255, blank=True, null=True)
    date_approved = models.DateTimeField(null=True, blank=True)
    create_date = models.DateTimeField("Date Created", null=True, blank=True)
    edit_date = models.DateTimeField("Last Edit Date", null=True, blank=True)
    latitude = models.CharField("Latitude (Coordinates)", max_length=255, blank=True, null=True)
    longitude = models.CharField("Longitude (Coordinates)", max_length=255, blank=True, null=True)


    class Meta:
        ordering = ('create_date',)
        permissions = (
            ("can_approve", "Can approve proposal"),
          )

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ProjectProposal, self).save()

    def agreement_count(self):
        agree_count = ProjectAgreement.objects.all().filter(project_proposal=self.id).count()
        return agree_count

    def complete_count(self):
        complete_count = ProjectComplete.objects.all().filter(project_proposal=self.id).count()
        return complete_count

    #displayed in admin templates
    def __unicode__(self):
        return self.project_name


class ProjectProposalAdmin(admin.ModelAdmin):
    list_display = ('project_name')
    display = 'project_name'


class ProjectAgreement(models.Model):
    program = models.ForeignKey(Program, related_name="agreement")
    date_of_request = models.DateTimeField("Date of Request", blank=True, null=True)
    project_name = models.CharField("Project Name", help_text='Please be specific in your name.  Consider that your Project Name includes WHO, WHAT, WHERE, HOW', max_length=255)
    project_type = models.ForeignKey(ProjectType, help_text='Please refer to Form 05 - Project Progress Summary', max_length=255, blank=True, null=True)
    project_activity = models.CharField("Project Activity", help_text='This should come directly from the activities listed in the Logframe', max_length=255, blank=True, null=True)
    project_description = models.TextField("Project Description", help_text='Description must meet the Criteria.  Will translate description into three languages: English, Dari and Pashto)', blank=True, null=True)
    community = models.ManyToManyField(Community, blank=True)
    community_rep = models.CharField("Community Representative", max_length=255, blank=True, null=True)
    community_rep_contact = models.CharField("Community Representative Contact", help_text='Can have mulitple contact numbers', max_length=255, blank=True, null=True)
    community_mobilizer = models.CharField("MC Community Mobilizer", max_length=255, blank=True, null=True)
    community_mobilizer_contact = models.CharField("MC Community Mobilizer Contact Number", max_length=255, blank=True, null=True)
    community_proposal = models.FileField("Community Proposal", upload_to='uploads', blank=True, null=True)
    has_rej_letter = models.BooleanField("If Rejected: Rejection Letter Sent?", help_text='If yes attach copy', default=False)
    rejection_letter = models.FileField("Rejection Letter", upload_to='uploads', blank=True, null=True)
    activity_code = models.CharField("Activity Code", help_text='If applicable at this stage, please request Activity Code from MEL', max_length=255, blank=True, null=True)
    office = models.ForeignKey(Office, null=True, blank=True)
    cod_num = models.CharField("Project COD #", max_length=255, blank=True, null=True)
    sector = models.ForeignKey("Sector", blank=True, null=True)
    external_stakeholder_list = models.FileField("External stakeholder list", help_text="Please refer to PM@MC Section 01: Identification and Design under 1.1", upload_to='uploads', blank=True, null=True)
    project_design = models.CharField("Activity design for", max_length=255, blank=True, null=True)
    account_code = models.CharField("Account Code", help_text='optional - request from finance', max_length=255, blank=True, null=True)
    lin_code = models.CharField("LIN Sub Code", help_text='optional - request from finance', max_length=255, blank=True, null=True)
    staff_responsible = models.CharField("MC Staff Responsible", max_length=255, blank=True, null=True)
    partners = models.BooleanField("Are there partners involved?", default=0)
    name_of_partners = models.CharField("Name of Partners", max_length=255, blank=True, null=True)
    program_objectives = models.TextField("What Program Objectives does this help fulfill?", blank=True, null=True)
    mc_objectives = models.TextField("What MC strategic Objectives does this help fulfill?", blank=True, null=True)
    effect_or_impact = models.TextField("What is the anticipated effect of impact of this project?", blank=True, null=True)
    expected_start_date = models.DateTimeField("Expected starting date", blank=True, null=True)
    expected_end_date = models.DateTimeField("Expected ending date",blank=True, null=True)
    expected_duration = models.CharField("Expected duration", help_text="[MONTHS]/[DAYS]", blank=True, null=True, max_length=255)
    beneficiary_type = models.CharField("Type of direct beneficiaries", help_text="i.e. Farmer, Association, Student, Govt, etc.", max_length=255, blank=True, null=True)
    estimated_num_direct_beneficiaries = models.CharField("Estimated number of direct beneficiaries", help_text="Please provide achievable estimates as we will use these as are 'Targets'",max_length=255, blank=True, null=True)
    average_household_size = models.CharField("Average Household Size", help_text="Refer to Form 01 - Community Profile",max_length=255, blank=True, null=True)
    estimated_num_indirect_beneficiaries = models.CharField("Estimated Number of indirect beneficiaries", help_text="This is a calculation - multiply direct beneficiaries by average household size",max_length=255, blank=True, null=True)
    total_estimated_budget = models.CharField(help_text="In USD", max_length=255, blank=True, null=True)
    mc_estimated_budget = models.CharField(help_text="In USD", max_length=255, blank=True, null=True)
    project_type_other = models.ForeignKey(ProjectTypeOther, blank=True, null=True)
    estimate_male_trained = models.IntegerField("Estimated # of Male Trained",blank=True,null=True)
    estimate_female_trained = models.IntegerField("Estimated # of Female Trained",blank=True,null=True)
    estimate_total_trained = models.IntegerField("Estimated Total # Trained",blank=True,null=True)
    estimate_trainings = models.IntegerField("Estimated # of Trainings Conducted",blank=True,null=True)
    distribution_type = models.CharField("Type of Items Distributed",max_length="255",null=True,blank=True)
    distribution_uom = models.CharField("Unit of Measure",max_length="255",null=True,blank=True)
    distribution_estimate = models.CharField("Estimated # of Items Distributed",max_length="255",null=True,blank=True)
    cfw_estimate_male = models.IntegerField("Estimated # of Male Laborers",blank=True,null=True)
    cfw_estimate_female = models.IntegerField("Estimated # of Female Laborers",blank=True,null=True)
    cfw_estimate_total = models.IntegerField("Estimated Total # of Laborers",blank=True,null=True)
    cfw_estimate_project_days = models.IntegerField("Estimated # of Project Days",blank=True,null=True)
    cfw_estimate_person_days = models.IntegerField("Estimated # of Person Days",blank=True,null=True)
    cfw_estimate_cost_materials = models.CharField("Estimated Total Cost of Materials",max_length="255",blank=True,null=True)
    cfw_estimate_wages_budgeted= models.CharField("Estimated Wages Budgeted",max_length="255",blank=True,null=True)
    estimation_date = models.DateTimeField(blank=True, null=True)
    estimated_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="estimating")
    estimated_by_date = models.DateTimeField("Date Estimated", null=True, blank=True)
    checked_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="checking")
    checked_by_date = models.DateTimeField("Date Checked", null=True, blank=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="reviewing")
    reviewed_by_date = models.DateTimeField("Date Reviewed", null=True, blank=True)
    finance_reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="finance_reviewing")
    finance_reviewed_by_date = models.DateTimeField("Date Reviewed by Finance", null=True, blank=True)
    me_reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="reviewing_me")
    me_reviewed_by_date = models.DateTimeField("Date Reviewed by M&E", null=True, blank=True)
    capacity = models.ManyToManyField(Capacity, blank=True)
    evaluate = models.ManyToManyField(Evaluate, blank=True)
    approval = models.CharField("Status", default="in progress", max_length=255, blank=True, null=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="approving_agreement")
    approved_by_date = models.DateTimeField("Date Approved", null=True, blank=True)
    approval_submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="submitted_by_agreement")
    approval_remarks = models.CharField("Approval Remarks", max_length=255, blank=True, null=True)
    justification_background = models.TextField("General background and problem statement", blank=True, null=True)
    justification_description_community_selection = models.TextField("Description of community selection criteria", blank=True, null=True)
    description_of_project_activities = models.TextField(blank=True, null=True)
    description_of_government_involvement = models.TextField(blank=True, null=True)
    description_of_community_involvement = models.TextField(blank=True, null=True)
    documentation_government_approval = models.FileField("Upload Government Documentation of Approval", upload_to='uploads', blank=True, null=True)
    documentation_community_approval = models.FileField("Upload Community Documentation of Approval", upload_to='uploads', blank=True, null=True)
    create_date = models.DateTimeField("Date Created", null=True, blank=True)
    edit_date = models.DateTimeField("Last Edit Date", null=True, blank=True)

    class Meta:
        ordering = ('create_date',)
        permissions = (
            ("can_approve", "Can approve agreement"),
        )

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ProjectAgreement, self).save()

    #displayed in admin templates
    def __unicode__(self):
        new_name = unicode(self.office) + unicode(" - ") + unicode(self.project_name)
        return new_name


class ProjectAgreementAdmin(admin.ModelAdmin):
    list_display = ('project_name')
    display = 'project_name'


class ProjectComplete(models.Model):
    program = models.ForeignKey(Program, null=True, blank=True, related_name="complete")
    project_agreement = models.ForeignKey(ProjectAgreement)
    activity_code = models.CharField("Activity Code", max_length=255, blank=True, null=True)
    project_name = models.CharField("Project Name", max_length=255, blank=True, null=True)
    project_activity = models.CharField("Project Activity", max_length=255, blank=True, null=True)
    office = models.ForeignKey(Office, null=True, blank=True)
    expected_start_date = models.DateTimeField(help_text="Comes from Form-04 Project Agreement", blank=True, null=True)
    expected_end_date = models.DateTimeField(help_text="Comes from Form-04 Project Agreement", blank=True, null=True)
    expected_duration = models.CharField("Expected Duration", max_length=255, help_text="Comes from Form-04 Project Agreement", blank=True, null=True)
    actual_start_date = models.DateTimeField(help_text="Comes from Form-04 Project Agreement", blank=True, null=True)
    actual_end_date = models.DateTimeField(blank=True, null=True)
    actual_duration = models.CharField(max_length=255, blank=True, null=True)
    on_time = models.BooleanField(default=None)
    no_explanation = models.TextField("If not on time explain delay", blank=True, null=True)
    estimated_budget = models.CharField("Estimated Budget", help_text="Comes from Form-04 Project Agreement", max_length=255, null=True, blank=True)
    actual_budget = models.CharField("Actual Budget", help_text="What was the actual final cost?  This should match any financial documentation you have in the file.   It should be completely documented and verifiable by finance and any potential audit", max_length=255, null=True, blank=True)
    budget_variance = models.CharField("Budget Variance", blank=True, null=True, max_length=255)
    explanation_of_variance = models.CharField("Explanation of variance", blank=True, null=True, max_length=255)
    direct_beneficiaries = models.CharField("Actual Direct Beneficiaries", max_length=255, blank=True, null=True)
    jobs_created = models.CharField("Number of Jobs Created", max_length=255, blank=True, null=True)
    jobs_part_time = models.CharField("Part Time Jobs", max_length=255, blank=True, null=True)
    jobs_full_time = models.CharField("Full Time Jobs", max_length=255, blank=True, null=True)
    government_involvement = models.CharField("Government Involvement", max_length=255, blank=True, null=True)
    capacity_built = models.CharField("What capacity was built to ensure sustainability?", max_length=255, blank=True, null=True)
    issues_and_challenges = models.TextField("List any issues or challenges faced (include reasons for delays)", blank=True, null=True)
    lessons_learned= models.TextField("Lessons learned", blank=True, null=True)
    community = models.ManyToManyField(Community, blank=True)
    estimated_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="estimating_complete")
    checked_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="checking_complete")
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="reviewing_complete")
    approval = models.CharField("Status", default="in progress", max_length=255, blank=True, null=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="approving_agreement_complete")
    approval_submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, related_name="submitted_by_complete")
    approval_remarks = models.CharField("Approval Remarks", max_length=255, blank=True, null=True)
    create_date = models.DateTimeField("Date Created", null=True, blank=True)
    edit_date = models.DateTimeField("Last Edit Date", null=True, blank=True)

    class Meta:
        ordering = ('create_date',)
        verbose_name_plural = "Activity Completions"

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ProjectComplete, self).save()

    #displayed in admin templates
    def __unicode__(self):
        new_name = unicode(self.office) + unicode(" - ") + unicode(self.project_name)
        return new_name


class ProjectCompleteAdmin(admin.ModelAdmin):
    list_display = ('program', 'project_name', 'activity_code')
    display = 'project_name'


class Documentation(models.Model):
    name = models.CharField("Name of Document", max_length=135, blank=True, null=True)
    url = models.CharField("URL (Link to document or document repository)", blank=True, null=True, max_length=135)
    description = models.CharField(max_length=255, blank=True, null=True)
    template = models.ForeignKey(Template, blank=True, null=True)
    file_field = models.FileField(upload_to="uploads", blank=True, null=True)
    project = models.ForeignKey(ProjectAgreement, blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

     #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Documentation, self).save()

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Documentation"


class DocumentationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'documentation_type', 'file_field', 'program_id', 'create_date', 'edit_date')
    display = 'Documentation'


class Benchmarks(models.Model):
    percent_complete = models.IntegerField("% complete", blank=True, null=True)
    percent_cumulative = models.IntegerField("% cumulative completion", blank=True, null=True)
    description = models.CharField("Description", max_length=255, blank=True)
    agreement = models.ForeignKey(ProjectAgreement,blank=True, null=True)
    complete = models.ForeignKey(ProjectComplete,blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('description',)
        verbose_name_plural = "Benchmarks"

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Benchmarks, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.description


class BenchmarksAdmin(admin.ModelAdmin):
    list_display = ('description', 'percent_complete', 'percent_cumulative', 'create_date', 'edit_date')
    display = 'Benchmarks'


class Monitor(models.Model):
    responsible_person = models.CharField("Person Responsible", max_length=25, blank=True, null=True)
    frequency = models.CharField("Frequency", max_length=25, blank=True, null=True)
    type = models.TextField("Type", null=True, blank=True)
    agreement = models.ForeignKey(ProjectAgreement,blank=True, null=True)
    complete = models.ForeignKey(ProjectComplete,blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('type',)
        verbose_name_plural = "Monitors"

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Monitor, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return self.responsible_person


class MonitorAdmin(admin.ModelAdmin):
    list_display = ('responsible_person', 'frequency', 'type', 'create_date', 'edit_date')
    display = 'Monitor'


class Budget(models.Model):
    contributor = models.CharField(max_length=135, blank=True, null=True)
    description_of_contribution = models.CharField(max_length=255, blank=True, null=True)
    proposed_value = models.IntegerField(default=0, blank=True, null=True)
    agreement = models.ForeignKey(ProjectAgreement, blank=True, null=True)
    complete = models.ForeignKey(ProjectComplete, blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    #onsave add create date or update edit date
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


class MergeMap(models.Model):
    project_agreement = models.ForeignKey(ProjectAgreement, null=True, blank=False)
    project_completion = models.ForeignKey(ProjectComplete, null=True, blank=False)
    from_column = models.CharField(max_length=255, blank=True)
    to_column = models.CharField(max_length=255, blank=True)


class MergeMapAdmin(admin.ModelAdmin):
    list_display = ('project_agreement', 'project_completion', 'from_column', 'to_column')
    display = 'project_agreement'


class ProgramDashboard(models.Model):
    program = models.ForeignKey(Program, null=True, blank=True)
    project_agreement = models.ForeignKey(ProjectAgreement, null=True, blank=True)
    project_completion = models.ForeignKey(ProjectComplete, null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('program',)

    #onsave add create date or update edit date
    def save(self):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ProgramDashboard, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return unicode("Program: %s " % (self.program, self.project_agreement))


class ProgramDashboardAdmin(admin.ModelAdmin):
    list_display = ('program', 'create_date', 'edit_date')
    display = 'Program Dashboard'


class TrainingAttendance(models.Model):
    training_name = models.CharField(max_length=255)
    program = models.ForeignKey(Program, null=True, blank=True)
    project_agreement = models.ForeignKey(ProjectAgreement, null=True, blank=True)
    implementer = models.CharField(max_length=255, null=True, blank=True)
    reporting_period = models.CharField(max_length=255, null=True, blank=True)
    total_participants = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    community = models.CharField(max_length=255, null=True, blank=True)
    training_duration = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.CharField(max_length=255, null=True, blank=True)
    end_date = models.CharField(max_length=255, null=True, blank=True)
    trainer_name = models.CharField(max_length=255, null=True, blank=True)
    trainer_contact_num = models.CharField(max_length=255, null=True, blank=True)
    form_filled_by = models.CharField(max_length=255, null=True, blank=True)
    form_filled_by_contact_num = models.CharField(max_length=255, null=True, blank=True)
    total_male = models.IntegerField(null=True, blank=True)
    total_female = models.IntegerField(null=True, blank=True)
    total_age_0_14_male = models.IntegerField(null=True, blank=True)
    total_age_0_14_female = models.IntegerField(null=True, blank=True)
    total_age_15_24_male = models.IntegerField(null=True, blank=True)
    total_age_15_24_female = models.IntegerField(null=True, blank=True)
    total_age_25_59_male = models.IntegerField(null=True, blank=True)
    total_age_25_59_female = models.IntegerField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('training_name',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(TrainingAttendance, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return unicode(self.training_name)


class TrainingAttendanceAdmin(admin.ModelAdmin):
    list_display = ('training_name', 'program', 'project_agreement', 'create_date', 'edit_date')
    display = 'Program Dashboard'


class Beneficiary(models.Model):
    beneficiary_name = models.CharField(max_length=255, null=True, blank=True)
    training = models.ForeignKey(TrainingAttendance, null=True, blank=True)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    community = models.ForeignKey(Community, null=True, blank=True)
    signature = models.BooleanField(default=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('beneficiary_name',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Beneficiary, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return unicode(self.beneficiary_name)


class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('beneficiary_name', 'father_name', 'age', 'gender', 'community', 'signature', 'remarks', 'initials')


class ChecklistItem(models.Model):
    item = models.CharField(max_length=255, null=True, blank=True)
    country = models.ForeignKey(Country,null=True,blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('item',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(ChecklistItem, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return unicode(self.item)


class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ('agreement')


class Checklist(models.Model):
    agreement = models.ForeignKey(ProjectAgreement, null=True, blank=True)
    item = models.ForeignKey(ChecklistItem, null=True, blank=True)
    in_file = models.BooleanField()
    not_applicable = models.BooleanField()
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('agreement',)

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Checklist, self).save()

    #displayed in admin templates
    def __unicode__(self):
        return unicode(self.agreement)


class ChecklistAdmin(admin.ModelAdmin):
    list_display = ('agreement')


# Documentation
class DocumentationApp(models.Model):
    name = models.CharField(max_length=255,null=True, blank=True)
    documentation = models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('create_date',)

    def save(self):
        if self.create_date is None:
            self.create_date = datetime.now()
        super(DocumentationApp, self).save()

    def __unicode__(self):
        return unicode(self.name)


class DocumentationAppAdmin(admin.ModelAdmin):
    list_display = ('name', 'documentation', 'create_date',)
    display = 'DocumentationApp'


# collect feedback from users
class Feedback(models.Model):
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL)
    note = models.TextField()
    page = models.CharField(max_length=135)
    severity = models.CharField(max_length=135)
    create_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('create_date',)

    def save(self):
        if self.create_date is None:
            self.create_date = datetime.now()
        super(Feedback, self).save()

    def __unicode__(self):
        return unicode(self.submitter)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('submitter', 'note', 'page', 'severity', 'create_date',)
    display = 'Feedback'


# FAQ
class FAQ(models.Model):
    question = models.TextField(null=True, blank=True)
    answer =  models.TextField(null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('create_date',)

    def save(self):
        if self.create_date is None:
            self.create_date = datetime.now()
        super(FAQ, self).save()

    def __unicode__(self):
        return unicode(self.question)


class FAQAdmin(admin.ModelAdmin):
    list_display = ( 'question', 'answer', 'create_date',)
    display = 'FAQ'


