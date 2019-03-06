from __future__ import unicode_literals

import json
import uuid

from django.db import models
from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.utils import timezone
from voluptuous import Schema, Required

from workflow.models import WorkflowLevel1, SiteProfile, WorkflowLevel2, Office, Organization
from indicators.models import DisaggregationValue, Indicator


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
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
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
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
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
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
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
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
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
    validations = models.CharField(max_length=500, null=True, blank=True)
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
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(CustomFormField, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode(self.name)


class CustomFormFieldAdmin(admin.ModelAdmin):
    list_display = ('name',)
    display = 'Custom Form Fields'
    list_filter = ('name',)


class CustomForm(models.Model):
    PUBLIC_ALL = 'all'  # deprecated
    PUBLIC_URL = 'url'  # deprecated

    PUBLIC_CHOICES = (  # deprecated
        (PUBLIC_ALL, 'ALL'),  # deprecated
        (PUBLIC_URL, 'URL'),  # deprecated
    )  # deprecated
    
    STATUS_ARCHIVED = 'archived'
    STATUS_NEW = 'new'
    STATUS_PUBLISHED = 'published'
    STATUS_UNPUBLISHED = 'unpublished'

    STATUS_CHOICES = (
        (STATUS_ARCHIVED, 'Archived'),
        (STATUS_NEW, 'New'),
        (STATUS_PUBLISHED, 'Published'),
        (STATUS_UNPUBLISHED, 'Unpublished'),
    )

    name = models.CharField(max_length=255, null=True, blank=True)
    form_uuid = models.CharField(max_length=255, verbose_name='CustomForm UUID', default=uuid.uuid4, unique=True)
    description = models.TextField(null=True, blank=True)
    validations = models.CharField(max_length=500, null=True, blank=True)
    fields = JSONField(blank=True, null=True)
    is_public = models.BooleanField(default=0)
    default_global = models.BooleanField(default=0)
    organization = models.ForeignKey(Organization, default=1)
    public = JSONField(blank=True, null=True, help_text="Public information with the structure:{org: (bool), url: (bool)}")
    workflowlevel1 = models.ForeignKey(WorkflowLevel1, blank=True, null=True)
    silo_id = models.IntegerField(default=0)
    status = models.CharField(blank=True, null=True, max_length=15, default=STATUS_NEW, choices=STATUS_CHOICES)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='customforms', null=True, blank=True, on_delete=models.SET_NULL)
    is_template = models.BooleanField(default=0)

    class Meta:
        ordering = ('name',)

    def _validate_public(self, public):
        schema = Schema({
            Required('org'): bool,
            Required('url'): bool
        })
        return schema(public)

    def clean_fields(self, exclude=None):
        super(CustomForm, self).clean_fields(exclude=exclude)
        if not self.is_template and self.public is not None:
            try:
                self.public = self._validate_public(self.public)
            except Exception as e:
                raise ValidationError(e)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        self.full_clean()
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
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