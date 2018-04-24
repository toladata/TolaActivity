import bisect
from collections import OrderedDict
from dateutil import rrule
from dateutil.relativedelta import relativedelta
from datetime import datetime
from django.core.urlresolvers import reverse_lazy
from django.db.models import Sum, Avg, Subquery, OuterRef, Case, When, Q, F, Min, Max
from django.views.generic import TemplateView, FormView
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseRedirect
from django.contrib import messages
from workflow.models import Program
from ..models import Indicator, CollectedData, Level, PeriodicTarget
from ..forms import IPTTReportQuickstartForm


class IPTTReportQuickstartView(FormView):
    template_name = 'indicators/iptt_quickstart.html'
    form_class = IPTTReportQuickstartForm
    FORM_PREFIX_TIME = 'timeperiods'
    FORM_PREFIX_TARGET = 'targetperiods'

    def get_context_data(self, **kwargs):
        context = super(IPTTReportQuickstartView, self).get_context_data(**kwargs)

        # Add two instances of the same form to context if they're not present
        if 'form' not in context:
            context['form'] = self.form_class(request=self.request, prefix=self.FORM_PREFIX_TIME)
        if 'form2' not in context:
            context['form2'] = self.form_class(request=self.request, prefix=self.FORM_PREFIX_TARGET)
        return context

    def get_form_kwargs(self):
        kwargs = super(IPTTReportQuickstartView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def post(self, request, *args, **kwargs):
        targetprefix = request.POST.get('%s-formprefix' % self.FORM_PREFIX_TARGET)
        timeprefix = request.POST.get('%s-formprefix' % self.FORM_PREFIX_TIME)

        # set prefix to the current form
        if targetprefix is not None:
            prefix = targetprefix
        else:
            prefix = timeprefix

        form = IPTTReportQuickstartForm(self.request.POST, prefix=prefix, request=self.request)

        # call the form_valid/invalid with the correct prefix and form
        if form.is_valid():
            return self.form_valid(**{'form': form, 'prefix': prefix})
        else:
            return self.form_invalid(**{'form': form, 'prefix': prefix})

    def form_valid(self, **kwargs):
        context = self.get_context_data()
        form = kwargs.get('form')
        prefix = kwargs.get('prefix')

        if prefix == self.FORM_PREFIX_TARGET:
            period = form.cleaned_data.get('targetperiods')
            context['form2'] = form
            context['form'] = self.form_class(request=self.request,
                                              prefix=self.FORM_PREFIX_TIME)
        else:
            prefix = self.FORM_PREFIX_TIME
            period = form.cleaned_data.get('timeperiods')
            context['form'] = form
            context['form2'] = self.form_class(request=self.request,
                                               prefix=self.FORM_PREFIX_TARGET)

        program = form.cleaned_data.get('program')
        num_recents = form.cleaned_data.get('numrecentperiods')
        redirect_url = reverse_lazy('iptt_report', kwargs={'program_id': program.id, 'reporttype': prefix})

        redirect_url = "{}?period={}&numrecents={}".format(redirect_url, period, num_recents)
        return HttpResponseRedirect(redirect_url)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data()
        form = kwargs.get('form')
        if kwargs.get('prefix') == self.FORM_PREFIX_TARGET:
            context['form2'] = form
            context['form'] = self.form_class(request=self.request, prefix=self.FORM_PREFIX_TIME)
        else:
            context['form'] = form
            context['form2'] = self.form_class(request=self.request, prefix=self.FORM_PREFIX_TARGET)
        return self.render_to_response(context)


class IPTT_ReportView(TemplateView):
    template_name = 'indicators/iptt_report.html'
    annotations = {}
    MONTHS_PER_MONTH = 1
    MONTHS_PER_QUARTER = 3
    MONTHS_PER_TRIANNUAL = 4
    MONTHS_PER_SEMIANNUAL = 6
    MONTHS_PER_YEAR = 12

    @staticmethod
    def _get_num_months(period):
        """
        Returns the number of months for a given time-period
        """
        try:
            return {
                1: IPTT_ReportView.MONTHS_PER_YEAR,
                2: IPTT_ReportView.MONTHS_PER_SEMIANNUAL,
                3: IPTT_ReportView.MONTHS_PER_TRIANNUAL,
                4: IPTT_ReportView.MONTHS_PER_QUARTER,
                5: IPTT_ReportView.MONTHS_PER_MONTH
                }[period]
        except KeyError:
            return 0

    @staticmethod
    def _get_period_name(period):
        """
        Returns the name of the period
        """
        try:
            return {
                1: 'Year',
                2: 'Semi-annual',
                3: 'Tri-annual',
                4: 'Quarter',
                5: 'Month'
            }[period]
        except KeyError:
            return 0

    def _get_first_period(self, start_date, num_months_in_period):
        if start_date is None:
            num_months_in_period = 0

        if num_months_in_period == IPTT_ReportView.MONTHS_PER_MONTH:
            # if interval is monthly, set the start_date to the first of the month
            period_start_date = start_date.replace(day=1)
        elif num_months_in_period == IPTT_ReportView.MONTHS_PER_QUARTER:
            # if interval is quarterly, set period_start_date to first calendar quarter
            quarter_start = [start_date.replace(month=month, day=1) for month in (1, 4, 7, 10)]
            index = bisect.bisect(quarter_start, start_date)
            period_start_date = quarter_start[index-1]
        elif num_months_in_period == IPTT_ReportView.MONTHS_PER_TRIANNUAL:
            # if interval is tri-annual, set period_start_date to first calendar tri-annual
            tri_annual_start = [start_date.replace(month=month, day=1) for month in (1, 5, 9)]
            index = bisect.bisect(tri_annual_start, start_date)
            period_start_date = tri_annual_start[index-1]
        elif num_months_in_period == IPTT_ReportView.MONTHS_PER_SEMIANNUAL:
            # if interval is semi-annual, set period_start_date to first calendar semi-annual
            semi_annual = [start_date.replace(month=month, day=1) for month in (1, 7)]
            index = bisect.bisect(semi_annual, start_date)
            period_start_date = semi_annual[index-1]
        elif num_months_in_period == IPTT_ReportView.MONTHS_PER_YEAR:
            # if interval is annual, set period_start_date to first calendar year
            period_start_date = start_date.replace(month=1, day=1)
        else:
            period_start_date = None

        return period_start_date

    def _generate_timperiod_annotations(self, timeperiods):
        """
        Generates queryset annotation(sum, avg, last data record). All three annotations are calculated
        because one of these three values will be used depending on how an indicator is configured.
        """
        last_data_record = CollectedData.objects.filter(indicator=OuterRef('pk')).order_by('-id')
        for k, v in timeperiods.items():
            annotation_sum = Sum(
                Case(
                    When(
                        Q(collecteddata__date_collected__gte=datetime.strftime(v[0], '%Y-%m-%d')) &
                        Q(collecteddata__date_collected__lte=datetime.strftime(v[1], '%Y-%m-%d')),
                        then=F('collecteddata__achieved')
                        )
                    )
                )

            annotation_avg = Avg(
                Case(
                    When(
                        Q(collecteddata__date_collected__gte=datetime.strftime(v[0], '%Y-%m-%d')) &
                        Q(collecteddata__date_collected__lte=datetime.strftime(v[1], '%Y-%m-%d')),
                        then=F('collecteddata__achieved')
                        )
                    )
                )

            annotation_last = Max(
                Case(
                    When(
                        Q(collecteddata__date_collected__gte=datetime.strftime(v[0], '%Y-%m-%d')) &
                        Q(collecteddata__date_collected__lte=datetime.strftime(v[1], '%Y-%m-%d')),
                        then=Subquery(last_data_record.values('achieved')[:1])
                        )
                    )
                )

            # the following becomes annotations for the queryset
            # e.g.
            # Year 1_sum=..., Year2_sum=..., etc.
            # Year 1_avg=..., Year2_avg=..., etc.
            # Year 1_last=..., Year2_last=..., etc.
            #
            self.annotations["{}_sum".format(k)] = annotation_sum
            self.annotations["{}_avg".format(k)] = annotation_avg
            self.annotations["{}_last".format(k)] = annotation_last
        return self.annotations

    def _get_num_periods(self, start_date, end_date, period):
        """
        Returns the number of periods depending on the period is in terms of months
        """
        num_months_in_period = self._get_num_months(period)
        total_num_months = len(list(rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date)))
        try:
            num_periods = total_num_months / num_months_in_period
            remainder_months = total_num_months % num_months_in_period
            if remainder_months > 0:
                num_periods += 1
        except ZeroDivisionError:
            num_periods = 0
        return num_periods

    def _generate_timeperiods(self, period_start_date, period, num_periods, num_recents):
        """
        Create date ranges for time-periods.
        """
        timeperiods = OrderedDict()
        if period_start_date is None:
            return timeperiods

        period_name = self._get_period_name(period)
        num_months_in_period = self._get_num_months(period)

        # if uesr specified num_recents periods then set it to retrieve only the last N entries
        if num_recents > 0:
            num_recents = num_periods - num_recents

        # bump up num_periods by 1 because the loop starts from 1 instead of 0
        num_periods += 1

        # calculate each period's start and end date
        for i in range(1, num_periods):
            if i > 1:
                # if it is not the first period then advance the
                # period_start_date by the correct number of months.
                period_start_date = period_start_date + relativedelta(months=+num_months_in_period)

            period_end_date = period_start_date + \
                relativedelta(months=+num_months_in_period) + relativedelta(days=-1)

            # do not include periods that are earlier than most_recent specified by user
            if i < num_recents:
                continue
            timeperiods["{} {}".format(period_name, i)] = [period_start_date, period_end_date]

        return timeperiods

    def _generate_targetperiod_annotations(self):
        """
        Generates annotations for periodic_targets
        """
        last_data_record = CollectedData.objects.filter(indicator=OuterRef('pk')).order_by('-id')
        annotation_sum = Sum(
            Case(
                When(
                    Q(collecteddata__date_collected__gte=F('periodictarget__start_date')) &
                    Q(collecteddata__date_collected__lte=F('periodictarget__end_date')),
                    then=F('collecteddata__achieved')
                )
            )
        )
        annotation_avg = Avg(
            Case(
                When(
                    Q(collecteddata__date_collected__gte=F('periodictarget__start_date')) &
                    Q(collecteddata__date_collected__lte=F('periodictarget__end_date')),
                    then=F('collecteddata__achieved')
                )
            )
        )
        annotation_last = Max(
            Case(
                When(
                    Q(collecteddata__date_collected__gte=F('periodictarget__start_date')) &
                    Q(collecteddata__date_collected__lte=F('periodictarget__end_date')),
                    then=Subquery(last_data_record.values('achieved')[:1])
                )
            )
        )
        self.annotations["target_sum"] = annotation_sum
        self.annotations["target_avg"] = annotation_avg
        self.annotations["target_last"] = annotation_last

        return self.annotations

    def get_context_data(self, **kwargs):
        context = super(IPTT_ReportView, self).get_context_data(**kwargs)
        reporttype = kwargs.get('reporttype')
        program_id = kwargs.get('program_id')

        try:
            period = int(self.request.GET.get('period', 1))
        except ValueError:
            period = 1  # default to annual interval

        try:
            num_recents = int(self.request.GET.get('numrecents', 0))
        except ValueError:
            num_recents = 0  # default to 0, which is all periods or targets

        try:
            program = Program.objects.get(pk=program_id)
        except Program.DoesNotExist:
            context['redirect'] = reverse_lazy('iptt_quickstart')
            messages.info(self.request, _("Please select a valid program."))
            return context

        # calculate aggregated actuals (sum, avg, last) per reporting period
        # (monthly, quarterly, tri-annually, seminu-annualy, and yearly) for each indicator
        lastlevel = Level.objects.filter(indicator__id=OuterRef('pk')).order_by('-id')
        last_data_record = CollectedData.objects.filter(indicator=OuterRef('pk')).order_by('-id')
        indicators = Indicator.objects.filter(program__in=[program_id])\
            .annotate(actualsum=Sum('collecteddata__achieved'),
                      actualavg=Avg('collecteddata__achieved'),
                      lastlevel=Subquery(lastlevel.values('name')[:1]),
                      lastdata=Subquery(last_data_record.values('achieved')[:1]))

        if reporttype == 'timeperiods':
            # determine the full date range of data collection for this program
            data_date_range = Indicator.objects.filter(program__in=[program_id])\
                .aggregate(sdate=Min('collecteddata__date_collected'), edate=Max('collecteddata__date_collected'))
            start_date = data_date_range['sdate']
            end_date = data_date_range['edate']

            try:
                # convert datetime to date object to avoid timezone issues in templates
                first_datacollected_date = start_date.date()
            except AttributeError:
                first_datacollected_date = None
                self.annotations = {}
                timeperiods = []
                report_start_date = None
                report_end_date = None

            if first_datacollected_date:
                num_periods = self._get_num_periods(start_date, end_date, period)
                num_months_in_period = self._get_num_months(period)
                report_start_date = self._get_first_period(first_datacollected_date, num_months_in_period)
                timeperiods = self._generate_timeperiods(report_start_date, period, num_periods, num_recents)
                report_end_date = timeperiods[timeperiods.keys()[-1]][1]
                self.annotations = self._generate_timperiod_annotations(timeperiods)

                # update the queryset with annotations for timeperiods
                indicators = indicators\
                    .values(
                        'id', 'number', 'name', 'program', 'lastlevel', 'unit_of_measure', 'direction_of_change',
                        'unit_of_measure_type', 'is_cumulative', 'baseline', 'lop_target', 'actualsum', 'actualavg',
                        'lastdata')\
                    .annotate(**self.annotations)

        elif reporttype == 'targetperiods':
            # get the full date range for periodic_targets setup for this program and period
            date_range = Indicator.objects.filter(program__in=[program_id], target_frequency=period).aggregate(
                sdate=Min('periodictarget__start_date'), edate=Max('periodictarget__end_date'))
            indicator_ids = indicators.values('id')
            pts = PeriodicTarget.objects.filter(indicator__in=indicator_ids)\
                .prefetch_related('indicator')\
                .values('id', 'period', 'target', 'indicator__name')\
                .annotate(actual_s=Sum('collecteddata__achieved'))
            report_start_date = date_range['sdate']
            report_end_date = date_range['edate']
        else:
            context['redirect'] = reverse_lazy('iptt_quickstart')
            messages.info(self.request, _("Please select a valid report type."))
            return context

        indicators = indicators.order_by('number', 'name')

        context['start_date'] = report_start_date
        context['end_date'] = report_end_date
        context['timeperiods'] = timeperiods
        context['indicators'] = indicators
        context['program'] = program
        context['reporttype'] = reporttype
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context.get('redirect', None):
            return HttpResponseRedirect(reverse_lazy('iptt_quickstart'))
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        pass
