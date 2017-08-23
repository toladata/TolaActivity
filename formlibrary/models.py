from __future__ import unicode_literals
from django.db import models
from django.contrib import admin
from datetime import datetime
from workflow.models import WorkflowLevel1, SiteProfile, WorkflowLevel2, Office, Province, Organization
from indicators.models import DisaggregationValue, Indicator
from django.contrib.postgres.fields import JSONField


try:
    from django.utils import timezone
except ImportError:
    from datetime import datetime as timezone


class TrainingAttendance(models.Model):
    training_name = models.CharField(max_length=255)
    workflowlevel1 = models.ForeignKey(WorkflowLevel1, null=True, blank=True)
    workflowlevel2 = models.ForeignKey(WorkflowLevel2, null=True, blank=True, verbose_name="Project Initiation")
    implementer = models.CharField(max_length=255, null=True, blank=True)
    training_indicator = models.ForeignKey(Indicator,blank=True,null=True)
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
    disaggregation_value = models.ManyToManyField(DisaggregationValue, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('training_name',)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(TrainingAttendance, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.training_name)


class TrainingAttendanceAdmin(admin.ModelAdmin):
    list_display = ('training_name', 'workflowlevel1', 'workflowlevel2', 'create_date', 'edit_date')
    display = 'Training Attendance'
    list_filter = ('workflowlevel1__country','workflowlevel1')


class Distribution(models.Model):
    distribution_name = models.CharField(max_length=255)
    workflowlevel1 = models.ForeignKey(WorkflowLevel1, null=True, blank=True)
    workflowlevel2 = models.ForeignKey(WorkflowLevel2, null=True, blank=True, verbose_name="Project Initiation")
    office_code = models.ForeignKey(Office, null=True, blank=True)
    distribution_indicator = models.ForeignKey(Indicator,blank=True,null=True)
    distribution_implementer = models.CharField(max_length=255, null=True, blank=True)
    reporting_period = models.CharField(max_length=255, null=True, blank=True)
    province = models.ForeignKey(Province, null=True, blank=True)
    total_beneficiaries_received_input = models.IntegerField(null=True, blank=True)
    distribution_location = models.CharField(max_length=255, null=True, blank=True)
    input_type_distributed = models.CharField(max_length=255, null=True, blank=True)
    distributor_name_and_affiliation = models.CharField(max_length=255, null=True, blank=True)
    distributor_contact_number = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    form_filled_by = models.CharField(max_length=255, null=True, blank=True)
    form_filled_by_position = models.CharField(max_length=255, null=True, blank=True)
    form_filled_by_contact_num = models.CharField(max_length=255, null=True, blank=True)
    form_filled_date = models.CharField(max_length=255, null=True, blank=True)
    form_verified_by = models.CharField(max_length=255, null=True, blank=True)
    form_verified_by_position = models.CharField(max_length=255, null=True, blank=True)
    form_verified_by_contact_num = models.CharField(max_length=255, null=True, blank=True)
    form_verified_date = models.CharField(max_length=255, null=True, blank=True)
    disaggregation_value = models.ManyToManyField(DisaggregationValue, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('distribution_name',)

    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Distribution, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.distribution_name)


class DistributionAdmin(admin.ModelAdmin):
    list_display = ('distribution_name', 'workflowlevel1', 'workflowlevel2', 'create_date', 'edit_date')
    display = 'Program Dashboard'


class Beneficiary(models.Model):
    beneficiary_name = models.CharField(max_length=255, null=True, blank=True)
    training = models.ManyToManyField(TrainingAttendance, blank=True)
    distribution = models.ManyToManyField(Distribution, blank=True)
    father_name = models.CharField(max_length=255, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    site = models.ForeignKey(SiteProfile, null=True, blank=True)
    signature = models.BooleanField(default=True)
    remarks = models.CharField(max_length=255, null=True, blank=True)
    workflowlevel1 = models.ManyToManyField(WorkflowLevel1, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('beneficiary_name',)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(Beneficiary, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.beneficiary_name)


class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('site','beneficiary_name',)
    display = 'Beneficiary'
    list_filter = ('site','beneficiary_name')


class FieldType(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(FieldType, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.name)


class FieldTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    display = 'Field Type'
    list_filter = ('name',)


class CustomFormField(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(default=0)
    type = models.ForeignKey(FieldType)
    required = models.BooleanField(default=0)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(CustomFormField, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.name)


class CustomFormFieldAdmin(admin.ModelAdmin):
    list_display = ('name',)
    display = 'Custom Form Fields'
    list_filter = ('name',)


class CustomForm(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    fields = JSONField(null=True)
    is_public = models.BooleanField(default=0)
    default_global = models.BooleanField(default=0)
    organization = models.ForeignKey(Organization, default=1)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = datetime.now()
        self.edit_date = datetime.now()
        super(CustomForm, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.name)


class CustomFormAdmin(admin.ModelAdmin):
    list_display = ('name',)
    display = 'Custom Forms'
    list_filter = ('name',)


class BinaryField(models.Model):
    # the field where data is stored
    name = models.CharField(max_length=255)
    data = models.BinaryField()