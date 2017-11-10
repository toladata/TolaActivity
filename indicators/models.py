from datetime import timedelta
from decimal import Decimal
import uuid

from django.db import models
from django.contrib import admin
from django.utils import timezone
from simple_history.models import HistoricalRecords

from search.exceptions import ValueNotFoundError
from workflow.models import WorkflowLevel1, Sector, SiteProfile, WorkflowLevel2, Country, Office, Documentation, TolaUser,\
    Organization


class TolaTable(models.Model):
    name = models.CharField(max_length=255, blank=True)
    table_id = models.IntegerField(blank=True, null=True)
    owner = models.ForeignKey('auth.User',blank=True, null=True)
    remote_owner = models.CharField(max_length=255, blank=True, null=True)
    country = models.ManyToManyField(Country, blank=True)
    workflowlevel1 = models.ManyToManyField(WorkflowLevel1, blank=True)
    organization = models.ForeignKey(Organization, default=1)
    url = models.CharField(max_length=255, blank=True)
    unique_count = models.IntegerField(blank=True, null=True)
    count_column_name_1 = models.CharField(max_length=255,blank=True, null=True)
    count_column_name_2 = models.CharField(max_length=255,blank=True, null=True)
    column_sum = models.IntegerField(default=0 ,blank=True, null=True)
    column_avg = models.IntegerField(default=0, blank=True, null=True)
    refresh_interval = models.IntegerField(default=0, blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(TolaTable, self).save(*args, **kwargs)


class TolaTableAdmin(admin.ModelAdmin):
    list_display = ('name','country','owner','url','create_date','edit_date')
    search_fields = ('country','name')
    list_filter = ('country__country',)
    display = 'Tola Table'


class IndicatorType(models.Model):
    indicator_type = models.CharField(max_length=135, blank=True)
    description = models.TextField(max_length=765, blank=True)
    default_global = models.BooleanField(default=0)
    organization = models.ForeignKey(Organization, default=1)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.indicator_type

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(IndicatorType, self).save(*args, **kwargs)


class IndicatorTypeAdmin(admin.ModelAdmin):
    list_display = ('indicator_type','description','create_date','edit_date')
    display = 'Indicator Type'


class StrategicObjective(models.Model):
    name = models.CharField(max_length=135, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True)
    description = models.TextField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True, blank=True)

    class Meta:
        ordering = ('country', 'name')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(StrategicObjective, self).save(*args, **kwargs)


class StrategicObjectiveAdmin(admin.ModelAdmin):
    list_display = ('country','name')
    search_fields = ('country__country','name')
    list_filter = ('country__country',)
    display = 'Strategic Objectives'


class Objective(models.Model):
    name = models.CharField(max_length=135, blank=True)
    workflowlevel1 = models.ForeignKey(WorkflowLevel1, null=True, blank=True)
    description = models.TextField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='objectives', null=True, blank=True)

    class Meta:
        ordering = ('workflowlevel1','name')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Objective, self).save(*args, **kwargs)


class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ('workflowlevel1','name')
    search_fields = ('name','workflowlevel1__name')
    list_filter = ('workflowlevel1__country__country',)
    display = 'Objectives'


class Level(models.Model):
    name = models.CharField(max_length=135, blank=True)
    workflowlevel1 = models.ForeignKey(WorkflowLevel1, null=True, blank=True)
    sort = models.IntegerField(default=0)
    country = models.ForeignKey(Country, null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True, blank=True)
    parent_id = models.IntegerField(default=0)
    global_default = models.BooleanField(default=0)
    description = models.TextField(max_length=765, blank=True)
    color = models.CharField(max_length=135, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='levels', null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        if not self.organization and self.workflowlevel1:
            self.organization = self.workflowlevel1.organization
        super(Level, self).save(*args, **kwargs)


class DisaggregationType(models.Model):
    disaggregation_type = models.CharField(max_length=135, blank=True)
    description = models.CharField(max_length=765, blank=True)
    organization = models.ForeignKey(Organization, default=0)
    standard = models.BooleanField(default=False, verbose_name="Standard")
    default_global = models.BooleanField(default=False)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.disaggregation_type

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(DisaggregationType, self).save(*args, **kwargs)


class DisaggregationTypeAdmin(admin.ModelAdmin):
    list_display = ('disaggregation_type','organization','standard','description')
    list_filter = ('organization','standard','disaggregation_type')
    display = 'Disaggregation Type'


class DisaggregationLabel(models.Model):
    disaggregation_type = models.ForeignKey(DisaggregationType)
    label = models.CharField(max_length=765, blank=True)
    customsort = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.label

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(DisaggregationLabel, self).save(*args, **kwargs)


class DisaggregationValue(models.Model):
    disaggregation_label = models.ForeignKey(DisaggregationLabel)
    value = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.value

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(DisaggregationValue, self).save(*args, **kwargs)


class DisaggregationValueAdmin(admin.ModelAdmin):
    list_display = ('disaggregation_label','value','create_date','edit_date')
    list_filter = ('disaggregation_label__disaggregation_type__disaggregation_type','disaggregation_label')
    display = 'Disaggregation Value'


class Frequency(models.Model):
    frequency = models.CharField(max_length=135, blank=True)
    description = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    numdays = models.PositiveIntegerField(default=0, verbose_name="Frequency in number of days")
    organization = models.ForeignKey(Organization, default=1)

    def __unicode__(self):
        return self.frequency

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Frequency, self).save(*args, **kwargs)


class ReportingPeriod(models.Model):
    frequency = models.ForeignKey(Frequency)
    organization = models.ForeignKey(Organization, default=1)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.frequency

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(ReportingPeriod, self).save(*args, **kwargs)


class ReportingPeriodAdmin(admin.ModelAdmin):
    list_display = ('frequency','create_date','edit_date')
    display = 'Reporting Frequency'


class ExternalService(models.Model):
    name = models.CharField(max_length=255, blank=True)
    service_url = models.CharField(max_length=765, blank=True)
    feed_url = models.CharField(max_length=765, blank=True)
    default_global = models.BooleanField(default=0)
    organization = models.ForeignKey(Organization, default=1)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        #onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(ExternalService, self).save(*args, **kwargs)


class ExternalServiceAdmin(admin.ModelAdmin):
    list_display = ('name','service_url','feed_url','create_date','edit_date')
    display = 'External Indicator Data Service'


class ExternalServiceRecord(models.Model):
    external_service = models.ForeignKey(ExternalService, blank=True, null=True)
    full_url = models.CharField(max_length=765, blank=True)
    record_id = models.CharField("Unique ID",max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.full_url

    def save(self, *args, **kwargs):
        #onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(ExternalServiceRecord, self).save(*args, **kwargs)


class ExternalServiceRecordAdmin(admin.ModelAdmin):
    list_display = ('external_service','full_url','record_id','create_date','edit_date')
    display = 'Exeternal Indicator Data Service'


class IndicatorManager(models.Manager):
    def get_queryset(self):
        return super(IndicatorManager, self).get_queryset().prefetch_related('workflowlevel1').select_related('sector')

from tola.security import SecurityModel
from search.utils import ElasticsearchIndexer

class Indicator(models.Model): # TODO change back to SecurityModel
    indicator_uuid = models.CharField(max_length=255,verbose_name='Indicator UUID', default=uuid.uuid4, unique=True, blank=True)
    indicator_type = models.ManyToManyField(IndicatorType, blank=True)
    level = models.ForeignKey(Level, null=True, blank=True, on_delete=models.SET_NULL)
    objectives = models.ManyToManyField(Objective, blank=True,verbose_name="Objective", related_name="obj_indicator")
    strategic_objectives = models.ManyToManyField(StrategicObjective, verbose_name="Country Strategic Objective", blank=True, related_name="strat_indicator")
    name = models.CharField(max_length=255, null=False)
    number = models.CharField(max_length=255, null=True, blank=True)
    source = models.CharField(max_length=255, null=True, blank=True)
    definition = models.TextField(null=True, blank=True)
    justification = models.TextField(max_length=500, null=True, blank=True, verbose_name="Rationale or Justification for Indicator")
    unit_of_measure = models.CharField(max_length=135, null=True, blank=True, verbose_name="Unit of Measure")
    disaggregation = models.ManyToManyField(DisaggregationType, blank=True)
    baseline = models.CharField(max_length=255, null=True, blank=True)
    lop_target = models.IntegerField("LOP Target",default=0, blank=True)
    rationale_for_target = models.TextField(max_length=255, null=True, blank=True)
    means_of_verification = models.CharField(max_length=255, null=True, blank=True, verbose_name="Means of Verification / Data Source")
    data_collection_method = models.CharField(max_length=255, null=True, blank=True, verbose_name="Data Collection Method")
    data_collection_frequency = models.ForeignKey(Frequency, related_name="data_collection_frequency",null=True, blank=True, verbose_name="Frequency of Data Collection")
    data_points = models.TextField(max_length=500, null=True, blank=True, verbose_name="Data Points")
    responsible_person = models.CharField(max_length=255, null=True, blank=True, verbose_name="Responsible Person(s) and Team")
    method_of_analysis = models.CharField(max_length=255, null=True, blank=True, verbose_name="Method of Analysis")
    information_use = models.CharField(max_length=255, null=True, blank=True, verbose_name="Information Use")
    reporting_frequency = models.ForeignKey(Frequency, null=True, blank=True, verbose_name="Frequency of Reporting")
    quality_assurance = models.TextField(max_length=500, null=True, blank=True, verbose_name="Quality Assurance Measures")
    data_issues = models.TextField(max_length=500, null=True, blank=True, verbose_name="Data Issues")
    indicator_changes = models.TextField(max_length=500, null=True, blank=True, verbose_name="Changes to Indicator")
    comments = models.TextField(max_length=255, null=True, blank=True)
    workflowlevel1 = models.ManyToManyField(WorkflowLevel1)
    sector = models.ForeignKey(Sector, null=True, blank=True)
    sub_sector = models.ManyToManyField(Sector, blank=True, related_name="indicator_sub_sector")
    key_performance_indicator = models.BooleanField("Key Performance Indicator?",default=False)
    approved_by = models.ForeignKey(TolaUser, blank=True, null=True, related_name="approving_indicator")
    approval_submitted_by = models.ForeignKey(TolaUser, blank=True, null=True, related_name="indicator_submitted_by")
    external_service_record = models.ForeignKey(ExternalServiceRecord, verbose_name="External Service ID", blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords()
    notes = models.TextField(max_length=500, null=True, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='indicators', null=True, blank=True)
    #optimize query for class based views etc.
    objects = IndicatorManager()

    class Meta:
        ordering = ('create_date',)
        permissions = (
            ('view_indicator', 'View Indicator Model'),
        )

    def save(self, *args, **kwargs):
        #onsave add create date or update edit date
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()

        super(Indicator, self).save(*args, **kwargs)

        ei = ElasticsearchIndexer()
        ei.index_indicator(self)

    def delete(self, *args, **kwargs):
        ei = ElasticsearchIndexer()
        try:
            ei.delete_indicator(self.id)
        except ValueNotFoundError:
            pass
        super(Indicator, self).delete(*args, **kwargs)

    @property
    def just_created(self):
        if self.create_date >= timezone.now() - timedelta(minutes=5):
            return True
        return False

    @property
    def name_clean(self):
        return self.name.encode('ascii', 'ignore')

    @property
    def objectives_list(self):
        return ', '.join([x.name for x in self.objectives.all()])

    @property
    def strategicobjectives_list(self):
        return ', '.join([x.name for x in self.strategic_objectives.all()])

    @property
    def programs(self):
        return ', '.join([x.name for x in self.workflowlevel1.all()])

    @property
    def indicator_types(self):
        return ', '.join([x.indicator_type for x in self.indicator_type.all()])

    @property
    def levels(self):
        #return ', '.join([x.name for x in self.level.all()])
        if self.level:
            return self.level.name
        return None

    @property
    def disaggregations(self):
        return ', '.join([x.disaggregation_type for x in self.disaggregation.all()])

    def __unicode__(self):
        return self.name



class PeriodicTarget(models.Model):
    indicator = models.ForeignKey(Indicator, null=False, blank=False)
    period = models.CharField(max_length=255, null=True, blank=True)
    target = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('0.00'))
    customsort = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.period, self.target)


class PeriodicTargetAdmin(admin.ModelAdmin):
    list_display = ('period', 'target', 'customsort',)
    display = 'Indicator Periodic Target'
    list_filter = ('period',)


class CollectedDataManager(models.Manager):
    def get_queryset(self):
        return super(CollectedDataManager, self).get_queryset().prefetch_related('site','disaggregation_value').select_related('workflowlevel1','indicator','workflowlevel2','evidence','tola_table')


class CollectedData(models.Model):
    data_uuid = models.CharField(max_length=255,verbose_name='Data UUID', default=uuid.uuid4, unique=True, blank=True)
    periodic_target = models.ForeignKey(PeriodicTarget, null=True, blank=True)
    #targeted = models.DecimalField("Targeted", max_digits=20, decimal_places=2, default=Decimal('0.00'))
    achieved = models.DecimalField("Achieved", max_digits=20, decimal_places=2, default=Decimal('0.00'))
    disaggregation_value = models.ManyToManyField(DisaggregationValue, blank=True)
    description = models.TextField("Remarks/comments", blank=True, null=True)
    indicator = models.ForeignKey(Indicator)
    workflowlevel2 = models.ForeignKey(WorkflowLevel2, blank=True, null=True, related_name="i_workflowlevel2", verbose_name="Project Initiation")
    workflowlevel1 = models.ForeignKey(WorkflowLevel1, blank=True, null=True, related_name="i_workflowlevel1")
    date_collected = models.DateTimeField(null=True, blank=True)
    comment = models.TextField("Comment/Explanation", max_length=255, blank=True, null=True)
    evidence = models.ForeignKey(Documentation, null=True, blank=True, verbose_name="Evidence Document or Link")
    approved_by = models.ForeignKey(TolaUser, blank=True, null=True, verbose_name="Originated By", related_name="approving_data")
    tola_table = models.ForeignKey(TolaTable, blank=True, null=True)
    update_count_tola_table = models.BooleanField("Would you like to update the achieved total with the row count from TolaTables?",default=False)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    site = models.ManyToManyField(SiteProfile, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='collecteddata', null=True, blank=True)
    history = HistoricalRecords()
    objects = CollectedDataManager()

    class Meta:
        ordering = ('workflowlevel2','indicator','date_collected','create_date')
        verbose_name_plural = "Indicator Output/Outcome Collected Data"

    #onsave add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date == None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(CollectedData, self).save(*args, **kwargs)

        ei = ElasticsearchIndexer()
        ei.index_collecteddata(self)

    def delete(self, *args, **kwargs):
        super(CollectedData, self).delete(*args, **kwargs)

        ei = ElasticsearchIndexer()
        ei.delete_collecteddata(self.data_uuid)

    #displayed in admin templates
    def __unicode__(self):
        return self.description

    def achieved_sum(self):
        achieved=CollectedData.targeted.filter(indicator__id=self).sum('achieved')
        return achieved

    @property
    def disaggregations(self):
        return ', '.join([y.disaggregation_label.label + ': ' + y.value for y in self.disaggregation_value.all()])



