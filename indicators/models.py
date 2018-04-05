import uuid
from datetime import timedelta
from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django.contrib import admin

from simple_history.models import HistoricalRecords

from workflow.models import (
    Program, Sector, SiteProfile, ProjectAgreement, ProjectComplete, Country,
    Documentation, TolaUser
)


class TolaTable(models.Model):
    name = models.CharField(_("name"), max_length=255, blank=True)
    table_id = models.IntegerField(_("table_id"), blank=True, null=True)
    owner = models.ForeignKey('auth.User', verbose_name=_("owner"))
    remote_owner = models.CharField(_("remote_owner"), max_length=255, blank=True)
    country = models.ManyToManyField(Country, blank=True, verbose_name=_("country"))
    url = models.CharField(_("url"), max_length=255, blank=True)
    unique_count = models.IntegerField(_("unique_count"), blank=True, null=True)
    create_date = models.DateTimeField(_("create_date"), null=True, blank=True)
    edit_date = models.DateTimeField(_("edit_date"), null=True, blank=True)

    def __unicode__(self):
        return self.name


class TolaTableAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'owner', 'url', 'create_date',
                    'edit_date')
    search_fields = ('country', 'name')
    list_filter = ('country__country',)
    display = 'Tola Table'


class IndicatorType(models.Model):
    indicator_type = models.CharField(_("indicator_type"), max_length=135, blank=True)
    description = models.TextField(_("description"), max_length=765, blank=True)
    create_date = models.DateTimeField(_("create_date"), null=True, blank=True)
    edit_date = models.DateTimeField(_("edit_date"), null=True, blank=True)

    class Meta:
        verbose_name = _("Indicator Type")

    def __unicode__(self):
        return self.indicator_type


class IndicatorTypeAdmin(admin.ModelAdmin):
    list_display = ('indicator_type', 'description', 'create_date',
                    'edit_date')
    display = 'Indicator Type'


class StrategicObjective(models.Model):
    name = models.CharField(_("name"), max_length=135, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True, verbose_name=_("country"))
    description = models.TextField(_("description"), max_length=765, blank=True)
    create_date = models.DateTimeField(_("create)_date"), null=True, blank=True)
    edit_date = models.DateTimeField(_("edit_date"), null=True, blank=True)

    class Meta:
        verbose_name = _("Strategic Objectives")
        ordering = ('country', 'name')

    def __unicode__(self):
        return self.name

    def save(self):
        if self.create_date is None:
            self.create_date = timezone.now()
        super(StrategicObjective, self).save()


class StrategicObjectiveAdmin(admin.ModelAdmin):
    list_display = ('country', 'name')
    search_fields = ('country__country', 'name')
    list_filter = ('country__country',)
    display = 'Strategic Objectives'


class Objective(models.Model):
    name = models.CharField(_("name"), max_length=135, blank=True)
    program = models.ForeignKey(Program, null=True, blank=True, verbose_name=_("program"))
    description = models.TextField(_("description"), max_length=765, blank=True)
    create_date = models.DateTimeField(_("create_date"), null=True, blank=True)
    edit_date = models.DateTimeField(_("edit_date"), null=True, blank=True)

    class Meta:
        verbose_name = _("Objective")
        ordering = ('program', 'name')

    def __unicode__(self):
        return self.name

    def save(self):
        if self.create_date is None:
            self.create_date = timezone.now()
        super(Objective, self).save()


class ObjectiveAdmin(admin.ModelAdmin):
    list_display = ('program', 'name')
    search_fields = ('name', 'program__name')
    list_filter = ('program__country__country',)
    display = 'Objectives'


class Level(models.Model):
    name = models.CharField(_("name"), max_length=135, blank=True)
    description = models.TextField(_("description"), max_length=765, blank=True)
    create_date = models.DateTimeField(_("create_date"), null=True, blank=True)
    edit_date = models.DateTimeField(_("edit_date"), null=True, blank=True)

    class Meta:
        verbose_name = ("Level")

    def __unicode__(self):
        return self.name

    def save(self):
        if self.create_date is None:
            self.create_date = timezone.now()
        super(Level, self).save()


class LevelAdmin(admin.ModelAdmin):
    list_display = ('name')
    display = 'Levels'


class DisaggregationType(models.Model):
    disaggregation_type = models.CharField(max_length=135, blank=True)
    description = models.CharField(max_length=765, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True)
    standard = models.BooleanField(
        default=False,
        verbose_name="Standard (TolaData Admins Only)"
    )
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.disaggregation_type


class DisaggregationTypeAdmin(admin.ModelAdmin):
    list_display = ('disaggregation_type', 'country', 'standard',
                    'description')
    list_filter = ('country', 'standard', 'disaggregation_type')
    display = 'Disaggregation Type'


class DisaggregationLabel(models.Model):
    disaggregation_type = models.ForeignKey(DisaggregationType)
    label = models.CharField(max_length=765, blank=True)
    customsort = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.label


class DisaggregationLabelAdmin(admin.ModelAdmin):
    list_display = ('disaggregation_type', 'customsort', 'label',)
    display = 'Disaggregation Label'
    list_filter = ('disaggregation_type__disaggregation_type',)


class DisaggregationValue(models.Model):
    disaggregation_label = models.ForeignKey(DisaggregationLabel)
    value = models.CharField(max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.value


class DisaggregationValueAdmin(admin.ModelAdmin):
    list_display = ('disaggregation_label', 'value', 'create_date',
                    'edit_date')
    list_filter = (
        'disaggregation_label__disaggregation_type__disaggregation_type',
        'disaggregation_label'
    )
    display = 'Disaggregation Value'


class ReportingFrequency(models.Model):
    frequency = models.CharField(_("frequency"), max_length=135, blank=True)
    description = models.CharField(_("description"), max_length=765, blank=True)
    create_date = models.DateTimeField(_("create_date"), null=True, blank=True)
    edit_date = models.DateTimeField(_("edit_date"), null=True, blank=True)

    class Meta:
        verbose_name = _("Reporting Frequency")

    def __unicode__(self):
        return self.frequency


class DataCollectionFrequency(models.Model):
    frequency = models.CharField(_("frequency"), max_length=135, blank=True, null=True)
    description = models.CharField(_("description"), max_length=255, blank=True, null=True)
    numdays = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Frequency in number of days")
    )
    create_date = models.DateTimeField(_("create_date"), null=True, blank=True)
    edit_date = models.DateTimeField(_("edit_date"), null=True, blank=True)

    class Meta:
        verbose_name = _("Data Collection Frequency")

    def __unicode__(self):
        return self.frequency


class DataCollectionFrequencyAdmin(admin.ModelAdmin):
    list_display = ('frequency', 'description', 'create_date', 'edit_date')
    display = 'Data Collection Frequency'


class ReportingPeriod(models.Model):
    frequency = models.ForeignKey(ReportingFrequency, verbose_name=_("frequency"))
    create_date = models.DateTimeField(_("create_date"), null=True, blank=True)
    edit_date = models.DateTimeField(_("edit_date"), null=True, blank=True)

    class Meta:
        verbose_name = _("Reporting Period")

    def __unicode__(self):
        return self.frequency


class ReportingPeriodAdmin(admin.ModelAdmin):
    list_display = ('frequency', 'create_date', 'edit_date')
    display = 'Reporting Frequency'


class ExternalService(models.Model):
    name = models.CharField(_("name"), max_length=255, blank=True)
    url = models.CharField(_("url"), max_length=765, blank=True)
    feed_url = models.CharField(_("feed_url"), max_length=765, blank=True)
    create_date = models.DateTimeField(_("create_date"), null=True, blank=True)
    edit_date = models.DateTimeField(_("edit_date"), null=True, blank=True)

    class Meta:
        verbose_name = _("External Service")

    def __unicode__(self):
        return self.name


class ExternalServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'feed_url', 'create_date', 'edit_date')
    display = 'External Indicator Data Service'


class ExternalServiceRecord(models.Model):
    external_service = models.ForeignKey(
        ExternalService, blank=True, null=True, verbose_name = _("external_service"))

    full_url = models.CharField(_("full_url"), max_length=765, blank=True)
    record_id = models.CharField(_("Unique ID"), max_length=765, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("External Service Record")

    def __unicode__(self):
        return self.full_url


class ExternalServiceRecordAdmin(admin.ModelAdmin):
    list_display = ('external_service', 'full_url', 'record_id', 'create_date',
                    'edit_date')
    display = 'Exeternal Indicator Data Service'


class IndicatorManager(models.Manager):
    def get_queryset(self):
        return super(IndicatorManager, self).get_queryset()\
            .prefetch_related('program')\
            .select_related('sector')


class Indicator(models.Model):
    LOP = 1
    MID_END = 2
    ANNUAL = 3
    SEMI_ANNUAL = 4
    TRI_ANNUAL = 5
    QUARTERLY = 6
    MONTHLY = 7
    EVENT = 8
    TARGET_FREQUENCIES = (
        (LOP, 'Life of Program (LoP) only'),
        (MID_END, 'Midline and endline'),
        (ANNUAL, 'Annual'),
        (SEMI_ANNUAL, 'Semi-annual'),
        (TRI_ANNUAL, 'Tri-annual'),
        (QUARTERLY, 'Quarterly'),
        (MONTHLY, 'Monthly'),
        (EVENT, 'Event')
    )

    NUMBER = 1
    PERCENTAGE = 2
    UNIT_OF_MEASURE_TYPES = (
        (NUMBER, 'Number (#)'),
        (PERCENTAGE, "Percentage (%)")
    )

    DIRECTION_OF_CHANGE_NONE = 1
    DIRECTION_OF_CHANGE_POSITIVE = 2
    DIRECTION_OF_CHANGE_NEGATIVE = 3
    DIRECTION_OF_CHANGE = (
        (DIRECTION_OF_CHANGE_NONE, "Direction of change (not applicable)"),
        (DIRECTION_OF_CHANGE_POSITIVE, "Positive (+)"),
        (DIRECTION_OF_CHANGE_NEGATIVE, "Negative (-)")
    )

    indicator_key = models.UUIDField(
        default=uuid.uuid4, unique=True, help_text=" "),

    indicator_type = models.ManyToManyField(
        IndicatorType, blank=True, help_text=" ", verbose_name=_("indicator_type"))

    level = models.ManyToManyField(Level, blank=True, help_text=" ", verbose_name=_("level"))

    objectives = models.ManyToManyField(
        Objective, blank=True, verbose_name=_("Program Objective"),
        related_name="obj_indicator", help_text=" "
    )

    strategic_objectives = models.ManyToManyField(
        StrategicObjective, verbose_name=_("Country Strategic Objective"),
        blank=True, related_name="strat_indicator", help_text=" "
    )

    name = models.CharField(verbose_name=_("Name"), max_length=255,
                            null=False, help_text=" ")

    number = models.CharField(_("number"), max_length=255, null=True, blank=True,
                              help_text=" ")

    source = models.CharField(_("source"), max_length=255, null=True, blank=True, help_text=" ")

    definition = models.TextField(_("definition"), null=True, blank=True, help_text=" ")

    justification = models.TextField(
        max_length=500, null=True, blank=True,
        verbose_name=_("Rationale or Justification for Indicator"), help_text=" "
    )

    unit_of_measure = models.CharField(
        max_length=135, null=True, blank=True, verbose_name=_("Unit of measure*"),
        help_text=" "
    )

    unit_of_measure_type = models.IntegerField(
        blank=False, null=True, choices=UNIT_OF_MEASURE_TYPES,
        default=UNIT_OF_MEASURE_TYPES[0][0],
        verbose_name=_("Unit Type"), help_text=" "
    )
    disaggregation = models.ManyToManyField(DisaggregationType, blank=True,
                                            help_text=" ", verbose_name=_("disaggregation"))
    baseline = models.CharField(
        verbose_name=_("Baseline*"), max_length=255, null=True, blank=True,
        help_text=" "
    )
    baseline_na = models.BooleanField(verbose_name=_("Not applicable"),
                                      default=False, help_text=" ")
    lop_target = models.CharField(
        verbose_name=_("Life of Program (LoP) target*"), max_length=255,
        null=True, blank=True, help_text=" "
    )
    direction_of_change = models.IntegerField(
        blank=False, null=True, choices=DIRECTION_OF_CHANGE,
        default=DIRECTION_OF_CHANGE[0][0],
        verbose_name=_("Direction of Chnage"), help_text=" ")

    is_cumulative = models.NullBooleanField(
        blank=False, verbose_name=_("C / NC"), help_text=" ")

    rationale_for_target = models.TextField(_("rationale_for_target"), max_length=255, null=True,
                                            blank=True, help_text=" ")
    target_frequency = models.IntegerField(
        blank=False, null=True, choices=TARGET_FREQUENCIES,
        verbose_name=_("Target frequency"), help_text=" "
    )
    target_frequency_custom = models.CharField(
        null=True, blank=True, max_length=100,
        verbose_name=_("First event name*"), help_text=" "
    )
    target_frequency_start = models.DateField(
        blank=True, null=True, auto_now=False,  auto_now_add=False,
        verbose_name=_("First target period begins*"), help_text=" "
    )
    target_frequency_num_periods = models.IntegerField(
        blank=True, null=True, verbose_name=_("Number of target periods*"),
        help_text=" "
    )
    means_of_verification = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name=_("Means of Verification / Data Source"), help_text=" "
    )
    data_collection_method = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name=_("Data Collection Method"), help_text=" "
    )
    data_collection_frequency = models.ForeignKey(
        DataCollectionFrequency, null=True, blank=True,
        verbose_name=_("Frequency of Data Collection"), help_text=" "
    )
    data_points = models.TextField(
        max_length=500, null=True, blank=True, verbose_name=_("Data Points"),
        help_text=" "
    )
    responsible_person = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name=_("Responsible Person(s) and Team"), help_text=" "
    )
    method_of_analysis = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name=_("Method of Analysis"), help_text=" "
    )
    information_use = models.CharField(
        max_length=255, null=True, blank=True,
        verbose_name=_("Information Use"), help_text=" "
    )
    reporting_frequency = models.ForeignKey(
        ReportingFrequency, null=True, blank=True,
        verbose_name=_("Frequency of Reporting"), help_text=" "
    )
    quality_assurance = models.TextField(
        max_length=500, null=True, blank=True,
        verbose_name=_("Quality Assurance Measures"), help_text=" "
    )
    data_issues = models.TextField(
        max_length=500, null=True, blank=True, verbose_name=_("Data Issues"),
        help_text=" "
    )
    indicator_changes = models.TextField(
        max_length=500, null=True, blank=True,
        verbose_name=_("Changes to Indicator"), help_text=" "
    )
    comments = models.TextField(_("comments"), max_length=255, null=True, blank=True,
                                help_text=" ")
    program = models.ManyToManyField(Program, help_text=" ", verbose_name=_("program"))
    sector = models.ForeignKey(Sector, null=True, blank=True, help_text=" ", verbose_name=_("sector"))
    key_performance_indicator = models.BooleanField(
        verbose_name=_("Key Performance Indicator for this program?"),
        default=False, help_text=" "
    )
    approved_by = models.ForeignKey(
        TolaUser, blank=True, null=True, related_name="approving_indicator",
        help_text=" "
    )
    approval_submitted_by = models.ForeignKey(
        TolaUser, blank=True, null=True, related_name="indicator_submitted_by",
        help_text=" "
    )
    external_service_record = models.ForeignKey(
        ExternalServiceRecord, verbose_name=_("External Service ID"),
        blank=True, null=True, help_text=" "
    )
    create_date = models.DateTimeField(null=True, blank=True, help_text=" ")
    edit_date = models.DateTimeField(null=True, blank=True, help_text=" ")
    history = HistoricalRecords()
    notes = models.TextField(_("notes"), max_length=500, null=True, blank=True)
    # optimize query for class based views etc.
    objects = IndicatorManager()

    class Meta:
        ordering = ('create_date',)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()
        super(Indicator, self).save(*args, **kwargs)

    @property
    def is_target_frequency_time_aware(self):
        return self.target_frequency in (self.ANNUAL, self.SEMI_ANNUAL,
                                         self.TRI_ANNUAL, self.QUARTERLY,
                                         self.MONTHLY)

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
        return ', '.join([x.name for x in self.program.all()])

    @property
    def indicator_types(self):
        return ', '.join([x.indicator_type for x in self.indicator_type.all()])

    @property
    def levels(self):
        return ', '.join([x.name for x in self.level.all()])

    @property
    def disaggregations(self):
        disaggregations = self.disaggregation.all()
        return ', '.join([x.disaggregation_type for x in disaggregations])

    @property
    def get_target_frequency_label(self):
        if self.target_frequency:
            return Indicator.TARGET_FREQUENCIES[self.target_frequency-1][1]
        return None


class PeriodicTarget(models.Model):
    indicator = models.ForeignKey(Indicator, null=False, blank=False)
    period = models.CharField(max_length=255, null=True, blank=True)

    target = models.DecimalField(
        max_digits=20, decimal_places=2, default=Decimal('0.00'))

    start_date = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True)

    end_date = models.DateField(
        auto_now=False, auto_now_add=False,  null=True, blank=True)

    customsort = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('customsort', '-create_date')

    def __unicode__(self):
        if self.indicator.target_frequency == Indicator.LOP \
            or self.indicator.target_frequency == Indicator.EVENT \
                or self.indicator.target_frequency == Indicator.MID_END:
            return self.period
        if self.start_date and self.end_date:
            return "%s (%s - %s)" % (self.period,
                                     self.start_date.strftime('%b %d, %Y'),
                                     self.end_date.strftime('%b %d, %Y'))
        return self.period

    @property
    def start_date_formatted(self):
        if self.start_date:
            return self.start_date.strftime('%b %d, %Y').replace(" 0", " ")
        return self.start_date

    @property
    def end_date_formatted(self):
        if self.end_date:
            return self.end_date.strftime('%b %d, %Y').replace(" 0", " ")
        return self.end_date


class PeriodicTargetAdmin(admin.ModelAdmin):
    list_display = ('period', 'target', 'customsort',)
    display = 'Indicator Periodic Target'
    list_filter = ('period',)


class CollectedDataManager(models.Manager):
    def get_queryset(self):
        return super(CollectedDataManager, self).get_queryset()\
            .prefetch_related('site', 'disaggregation_value')\
            .select_related('program', 'indicator', 'agreement', 'complete',
                            'evidence', 'tola_table')


class CollectedData(models.Model):
    data_key = models.UUIDField(
        default=uuid.uuid4, unique=True, help_text=" "),

    periodic_target = models.ForeignKey(
        PeriodicTarget, null=True, blank=True, help_text=" ")

    achieved = models.DecimalField(
        verbose_name="Actual", max_digits=20, decimal_places=2, help_text=" ")

    cumulative_achieved = models.DecimalField(
        verbose_name='Cumulative Actuals', max_digits=20, decimal_places=2,
        null=True, blank=True, help_text=" ")

    disaggregation_value = models.ManyToManyField(
        DisaggregationValue, blank=True, help_text=" ")

    description = models.TextField(
        "Remarks/comments", blank=True, null=True, help_text=" ")

    indicator = models.ForeignKey(Indicator, help_text=" ")

    agreement = models.ForeignKey(
        ProjectAgreement, blank=True, null=True, related_name="q_agreement2",
        verbose_name="Project Initiation", help_text=" ")

    complete = models.ForeignKey(
        ProjectComplete, blank=True, null=True, related_name="q_complete2",
        on_delete=models.SET_NULL, help_text=" ")

    program = models.ForeignKey(
        Program, blank=True, null=True, related_name="i_program",
        help_text=" ")

    date_collected = models.DateTimeField(
        null=True, blank=True, help_text=" ")

    comment = models.TextField(
        "Comment/Explanation", max_length=255, blank=True, null=True,
        help_text=" ")

    evidence = models.ForeignKey(
        Documentation, null=True, blank=True,
        verbose_name="Evidence Document or Link", help_text=" ")

    approved_by = models.ForeignKey(
        TolaUser, blank=True, null=True, verbose_name="Originated By",
        related_name="approving_data", help_text=" ")

    tola_table = models.ForeignKey(
        TolaTable, blank=True, null=True, help_text=" ")

    update_count_tola_table = models.BooleanField(
        verbose_name="Would you like to update the achieved total with the \
        row count from TolaTables?", default=False, help_text=" ")

    create_date = models.DateTimeField(null=True, blank=True, help_text=" ")
    edit_date = models.DateTimeField(null=True, blank=True, help_text=" ")
    site = models.ManyToManyField(SiteProfile, blank=True, help_text=" ")
    history = HistoricalRecords()
    objects = CollectedDataManager()

    class Meta:
        ordering = ('indicator', 'create_date', 'date_collected')
        verbose_name_plural = "Indicator Output/Outcome Collected Data"

    def __unicode__(self):
        return self.description

    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.now()
        self.edit_date = timezone.now()

        if self.achieved is not None:
            # calculate the cumulative sum of achieved value
            total_achieved = CollectedData.objects.filter(
                    indicator=self.indicator,
                    create_date__lt=self.create_date)\
                .aggregate(Sum('achieved'))['achieved__sum']

            if total_achieved is None:
                total_achieved = 0

            total_achieved = total_achieved + self.achieved
            self.cumulative_achieved = total_achieved
        super(CollectedData, self).save()

    def achieved_sum(self):
        achieved = CollectedData.targeted.filter(indicator__id=self)\
            .sum('achieved')
        return achieved

    @property
    def date_collected_formatted(self):
        if self.date_collected:
            return self.date_collected.strftime('%b %d, %Y').replace(" 0", " ")
        return self.date_collected

    @property
    def disaggregations(self):
        disaggs = self.disaggregation_value.all()
        return ', '.join([y.disaggregation_label.label + ': ' + y.value for y
                         in disaggs])

@receiver(post_delete, sender=CollectedData)
def model_post_delete(sender, **kwargs):
    instance = kwargs.get('instance', None)
    # print('Deleted: {}'.format(kwargs['instance'].__dict__))

    # the cumulative_achieved values need to be recalculated after an a
    # CollectedData record is deleted
    collecteddata = CollectedData.objects.filter(
            indicator=instance.indicator)\
        .order_by('id')

    # by saving each data reecord the cumulative_achieved is recalculated in
    # the save method of the CollectedData model class.
    for c in collecteddata:
        c.save()


class CollectedDataAdmin(admin.ModelAdmin):
    list_display = ('indicator', 'date_collected', 'create_date', 'edit_date')
    list_filter = ['indicator__program__country__country']
    display = 'Indicator Output/Outcome Collected Data'
