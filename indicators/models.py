from datetime import timedelta
from decimal import Decimal
import uuid

from django.db import models
from django.contrib import admin
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from simple_history.models import HistoricalRecords

from search.exceptions import ValueNotFoundError
from search.utils import ElasticsearchIndexer
from workflow.models import (WorkflowLevel1, Sector, SiteProfile,
                             WorkflowLevel2, Country, Documentation, TolaUser,
                             Organization)


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
    formula = JSONField(blank=True, null=True)
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
    name = models.CharField(max_length=135, blank=True, help_text="Organizational objective to associate with inidicator")
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
    name = models.CharField(max_length=135, blank=True, help_text="Objective for workflowleve1 to associate with indicator")
    workflowlevel1 = models.ForeignKey(WorkflowLevel1, null=True, blank=True)
    description = models.TextField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='objectives', null=True, blank=True, on_delete=models.SET_NULL)

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
    name = models.CharField(max_length=135, blank=True,help_text="Results framework or general indicator collection or label for level")
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
    created_by = models.ForeignKey('auth.User', related_name='levels', null=True, blank=True, on_delete=models.SET_NULL)

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
    AVAILABLE_ORG = 'org'
    AVAILABLE_WFL1 = 'wfl1'
    AVAILABILITY_CHOICES = (
        (AVAILABLE_ORG, 'Organization Level'),
        (AVAILABLE_WFL1, 'Only for this WFL1')
    )

    availability = models.CharField(choices=AVAILABILITY_CHOICES, max_length=5, null=True, blank=True)
    disaggregation_type = models.CharField(max_length=135, blank=True, help_text="Data disaggregation by age,gender,location etc.")
    description = models.CharField(max_length=765, blank=True)
    organization = models.ForeignKey(Organization, default=0)
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
    list_display = ('disaggregation_type', 'organization', 'availability', 'description')
    list_filter = ('organization', 'availability', 'disaggregation_type')
    display = 'Disaggregation Type'


class DisaggregationLabel(models.Model):
    disaggregation_type = models.ForeignKey(DisaggregationType, on_delete=models.deletion.PROTECT)
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
    disaggregation_label = models.ForeignKey(DisaggregationLabel, on_delete=models.deletion.PROTECT)
    indicator = models.ForeignKey('indicators.Indicator', null=True, blank=True)
    value = models.CharField(max_length=765, blank=True)
    table_uuid = models.CharField(max_length=36, blank=True)
    column_name = models.CharField(max_length=24, blank=True)
    column_value = models.CharField(max_length=24, blank=True)
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
    period = models.CharField(max_length=255, blank=True, null=True, help_text="Predefined reporting period for a workflowlevel1")
    workflowlevel1 = models.ForeignKey(WorkflowLevel1, null=True, blank=True, help_text="Related workflowlevel1 or project/program etc.")
    sort = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.period

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date is None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(ReportingPeriod, self).save(*args, **kwargs)


class ReportingPeriodAdmin(admin.ModelAdmin):
    list_display = ('frequency','create_date','edit_date')
    display = 'Reporting Frequency'


class ExternalService(models.Model):
    name = models.CharField(max_length=255, blank=True, help_text="External Indicator service for template of an Indicator instance")
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


class Indicator(models.Model):
    CALC_TYPE_NUMERIC = 'numeric'
    CALC_TYPE_PERCENTAGE = 'percentage'

    CALCULATION_CHOICES = (
        (CALC_TYPE_NUMERIC, 'Numeric'),
        (CALC_TYPE_PERCENTAGE, 'Percentage'),
    )

    DIRECTION_INCREASING = 'increasing'
    DIRECTION_DECREASING = 'decreasing'

    DIRECTION_CHOICES = (
        (DIRECTION_INCREASING, 'Increasing'),
        (DIRECTION_DECREASING, 'Decreasing'),
    )

    ACTUAL_FORMULA_AVG = 'average'
    ACTUAL_FORMULA_USER_DEFINED = 'user_defined'

    ACTUAL_FORMULA_CHOICES = (
        (ACTUAL_FORMULA_AVG, 'Average'),
        (ACTUAL_FORMULA_USER_DEFINED, 'User defined'),
    )

    indicator_uuid = models.CharField(max_length=255,verbose_name='Indicator UUID', default=uuid.uuid4, unique=True, blank=True)
    indicator_type = models.ManyToManyField(IndicatorType, blank=True, help_text="If indicator was pulled from a service select one here")
    level = models.ForeignKey(Level, null=True, blank=True, on_delete=models.SET_NULL, help_text="The results framework level goal, objective etc. for this indicator")
    objectives = models.ManyToManyField(Objective, blank=True,verbose_name="Objective", related_name="obj_indicator", help_text="Internal stated objective")
    strategic_objectives = models.ManyToManyField(StrategicObjective, verbose_name="Country Strategic Objective", blank=True, related_name="strat_indicator", help_text="Organizational objectives")
    name = models.CharField(max_length=255, null=False)
    number = models.CharField(max_length=255, null=True, blank=True, help_text="Internal organizational structure for relating to indicator and level")
    source = models.CharField(max_length=255, null=True, blank=True, help_text="Origin of indicator")
    definition = models.TextField(null=True, blank=True, help_text="Descriptive text for broader definiton and goal")
    justification = models.TextField(max_length=500, null=True, blank=True, verbose_name="Rationale or Justification for Indicator", help_text="Rationale or Justification for Indicator")
    unit_of_measure = models.CharField(max_length=135, null=True, blank=True, verbose_name="Unit of Measure", help_text="How will progress be measured")
    disaggregation = models.ManyToManyField(DisaggregationType, blank=True, help_text="Predefined units to split total actauls")
    baseline = models.CharField(max_length=255, null=True, blank=True, help_text="Initial set of data used for comparison or a control")
    lop_target = models.DecimalField("LOP Target", max_digits=20, decimal_places=4, default=Decimal('0.0000'), blank=True, help_text="Life of Program or Project goal for actual")
    rationale_for_target = models.TextField(max_length=255, null=True, blank=True, help_text="Reasoning for why the target value was set")
    means_of_verification = models.CharField(max_length=255, null=True, blank=True, verbose_name="Means of Verification / Data Source", help_text="Means of Verification / Data Source")
    data_collection_method = models.CharField(max_length=255, null=True, blank=True, verbose_name="Data Collection Method", help_text="How was the data collected")
    data_collection_frequency = models.ForeignKey(Frequency, related_name="data_collection_frequency",null=True, blank=True, verbose_name="Frequency of Data Collection", help_text="How often was the data collected")
    data_points = models.TextField(max_length=500, null=True, blank=True, verbose_name="Data Points", help_text="")
    responsible_person = models.CharField(max_length=255, null=True, blank=True, verbose_name="Responsible Person(s) and Team", help_text="Responsible Person(s) and Team")
    method_of_analysis = models.CharField(max_length=255, null=True, blank=True, verbose_name="Method of Analysis", help_text="Method of Analysis")
    information_use = models.CharField(max_length=255, null=True, blank=True, verbose_name="Information Use", help_text="Information Use")
    reporting_frequency = models.ForeignKey(Frequency, null=True, blank=True, verbose_name="Frequency of Reporting", help_text="Frequency of Reporting")
    quality_assurance = models.TextField(max_length=500, null=True, blank=True, verbose_name="Quality Assurance Measures", help_text="Quality Assurance Measures")
    data_issues = models.TextField(max_length=500, null=True, blank=True, verbose_name="Data Issues", help_text="Problems with the data quality if any")
    indicator_changes = models.TextField(max_length=500, null=True, blank=True, verbose_name="Changes to Indicator", help_text="How did the indicator change over time if at all")
    comments = models.TextField(max_length=255, null=True, blank=True, help_text="")
    workflowlevel1 = models.ManyToManyField(WorkflowLevel1, help_text="Related workflowlevel1 or project/program etc.")
    sector = models.ForeignKey(Sector, null=True, blank=True, help_text="Primary related sector or type of work done")
    sub_sector = models.ManyToManyField(Sector, blank=True, related_name="indicator_sub_sector", help_text="Additiona related sectors or type of work if any")
    key_performance_indicator = models.BooleanField("Key Performance Indicator?",default=False, help_text="Yes/No is this a key measurement for the overall effort")
    approved_by = models.ForeignKey(TolaUser, blank=True, null=True, related_name="approving_indicator", help_text="Who approved the indicator")
    approval_submitted_by = models.ForeignKey(TolaUser, blank=True, null=True, related_name="indicator_submitted_by", help_text="Who requested approval of the indicator")
    external_service_record = models.ForeignKey(ExternalServiceRecord, verbose_name="External Service ID", blank=True, null=True, help_text="What third party indicator service was this pulled from if any")
    create_date = models.DateTimeField(null=True, blank=True, help_text="")
    edit_date = models.DateTimeField(null=True, blank=True, help_text="")
    history = HistoricalRecords()
    notes = models.TextField(max_length=500, null=True, blank=True, help_text="")
    created_by = models.ForeignKey('auth.User', related_name='indicators', null=True, blank=True, on_delete=models.SET_NULL)
    objects = IndicatorManager()
    calculation_type = models.CharField(blank=True, null=True, max_length=15, choices=CALCULATION_CHOICES)
    direction = models.CharField(blank=True, null=True, max_length=15, choices=DIRECTION_CHOICES)
    actual_formula = models.CharField(blank=True, null=True, max_length=15)
    actuals = models.DecimalField(max_digits=20, decimal_places=4,blank=True, null=True, help_text="Sum of collected datas achieved")
    total_actual = models.ForeignKey('CollectedData', related_name='indicator_total_actual', on_delete=models.SET_NULL, verbose_name="Total Actual", blank=True, null=True, help_text="The collected data selected to be used in the actual formula")

    class Meta:
        ordering = ('create_date',)
        permissions = (
            ('view_indicator', 'View Indicator Model'),
        )

    def save(self, *args, **kwargs):
        # onsave add create date or update edit date
        if self.create_date is None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()

        super(Indicator, self).save(*args, **kwargs)

        ei = ElasticsearchIndexer()
        ei.index_indicator(self)

    def delete(self, *args, **kwargs):
        ei = ElasticsearchIndexer()
        try:
            ei.delete_indicator(self)
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
    target = models.DecimalField(max_digits=20, decimal_places=4, default=Decimal('0.0000'))
    customsort = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.period, self.target)


class CollectedDataManager(models.Manager):
    def get_queryset(self):
        return super(CollectedDataManager, self).get_queryset().prefetch_related('site','disaggregation_value').select_related('workflowlevel1','indicator','workflowlevel2','evidence','tola_table')


class CollectedData(models.Model):
    data_uuid = models.CharField(max_length=255,verbose_name='Data UUID', default=uuid.uuid4, unique=True, blank=True, help_text="")
    periodic_target = models.ForeignKey(PeriodicTarget, null=True, blank=True, help_text="Relate this collection to a periodic target")
    #targeted = models.DecimalField("Targeted", max_digits=20, decimal_places=2, default=Decimal('0.00'))
    achieved = models.DecimalField("Achieved", max_digits=20, decimal_places=4, default=Decimal('0.0000'), help_text="Actual or total for this record")
    disaggregation_value = models.ManyToManyField(DisaggregationValue, blank=True, help_text="Values for each disaggregated field")
    description = models.TextField("Remarks/comments", blank=True, null=True, help_text="How was this data collected")
    indicator = models.ForeignKey(Indicator, help_text="Related indicator for this data")
    workflowlevel2 = models.ForeignKey(WorkflowLevel2, blank=True, null=True, related_name="i_workflowlevel2", verbose_name="Project Initiation", help_text="Related workflowlevel1 for this data if no indicator")
    workflowlevel1 = models.ForeignKey(WorkflowLevel1, blank=True, null=True, related_name="i_workflowlevel1", help_text="Related workflowlevel1 if no workflowlevel 2 for this data and no indicator")
    date_collected = models.DateTimeField(null=True, blank=True, help_text="")
    comment = models.TextField("Comment/Explanation", max_length=255, blank=True, null=True)
    evidence = models.ForeignKey(Documentation, null=True, blank=True, verbose_name="Evidence Document or Link", help_text="Evidence Document or Link")
    evidence_url = models.CharField(max_length=255, null=True, blank=True, verbose_name="Evidence Document url", help_text="Evidence Document url")
    approved_by = models.ForeignKey(TolaUser, blank=True, null=True, verbose_name="Approved By", related_name="approving_data", help_text="Who approved collection")
    tola_table = models.ForeignKey(TolaTable, blank=True, null=True, help_text="If Track table was used link to it here")
    update_count_tola_table = models.BooleanField("Would you like to update the achieved total with the row count from TolaTables?",default=False, help_text="Update the unique count from Table if linked when updated")
    table_uuid = models.CharField(max_length=255, blank=True, null=True, help_text="Track service table url")
    formula = models.CharField(max_length=20, blank=True, null=True, help_text="Formula")
    column_name = models.CharField(max_length=64, blank=True, null=True, help_text="Formula")
    conditions = JSONField(blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    site = models.ManyToManyField(SiteProfile, blank=True, help_text="Geographic location for data source")
    cell_value = models.CharField(max_length=24, blank=True, null=True)
    created_by = models.ForeignKey('auth.User', related_name='collecteddata', null=True, blank=True, on_delete=models.SET_NULL)
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
        ei.delete_collecteddata(self)

    #displayed in admin templates
    def __unicode__(self):
        return self.description

    def achieved_sum(self):
        achieved=CollectedData.targeted.filter(indicator__id=self).sum('achieved')
        return achieved

    @property
    def disaggregations(self):
        return ', '.join([y.disaggregation_label.label + ': ' + y.value for y in self.disaggregation_value.all()])



