from collections import OrderedDict
from dateutil import rrule, relativedelta
from datetime import datetime
from django.core.urlresolvers import reverse_lazy
from django.db.models import Sum, Avg, Subquery, OuterRef, Case, When, Q, F, Min, Max
from django.views.generic import TemplateView, FormView
from django.http import HttpResponseRedirect
from workflow.models import Program
from ..models import Indicator, CollectedData, Level
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

    @staticmethod
    def _get_num_months(period):
        """
        Returns the number of months for a given time-period
        """
        return {'1': 12, '2': 6, '3': 4, '4': 3, '5': 1}[period]

    @staticmethod
    def _get_period_name(period):
        """
        Returns the name of the period
        """
        return {
            '1': 'Year',
            '2': 'Semi-annual',
            '3': 'Tri-annual',
            '4': 'Quarter',
            '5': 'Month'
        }[period]

    def _generate_timperiod_annotations(self, timeperiods):
        """
        Generates queryset annotation(sum, avg, last data record). All three annotations are calculated
        because one of these three values will be used depending on how an indicator is configured.
        """
        annotations = {}
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
            annotations["{}_sum".format(k)] = annotation_sum
            annotations["{}_avg".format(k)] = annotation_avg
            annotations["{}_last".format(k)] = annotation_last
        return annotations

    def _get_num_periods(self, start_date, end_date, period):
        """
        Returns the number of periods depending on the period is in terms of months
        """
        num_months_in_period = self._get_num_months(period)
        total_num_months = len(list(rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date)))
        num_periods = total_num_months / num_months_in_period
        remainder_months = total_num_months % num_months_in_period
        if remainder_months > 0:
            num_periods += 1
        return num_periods

    def _generate_timeperiods(self, start_date, period, num_periods, num_recents):
        """
        Create the time-periods for which data will be annotated
        """
        timeperiods = OrderedDict()
        period_name = self._get_period_name(period)
        num_months_in_period = self._get_num_months(period)

        period_start_date = start_date
        period_end_date = period_start_date + relativedelta.relativedelta(months=num_months_in_period)

        for i in range(num_recents, num_periods):
            timeperiods["{} {}".format(period_name, i)] = [period_start_date, period_end_date]
            period_start_date = period_end_date
            period_end_date = period_end_date + relativedelta.relativedelta(months=num_months_in_period)
        return timeperiods

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        program_id = kwargs.get('program_id')
        period = request.GET.get('period', None)
        try:
            num_recents = int(request.GET.get('numrecents', 1))
        except Exception:
            num_recents = 1
        program = Program.objects.get(pk=program_id)

        # determine the full date range of data collection for this program
        data_date_range = Indicator.objects.filter(program__in=[program_id])\
            .aggregate(sdate=Min('collecteddata__date_collected'), edate=Max('collecteddata__date_collected'))
        start_date = data_date_range['sdate']
        end_date = data_date_range['edate']

        #  find out the total number of periods (quarters, months, years, or etc) for this program
        num_periods = self._get_num_periods(start_date, end_date, period)

        timeperiods = self._generate_timeperiods(start_date, period, num_periods, num_recents)
        timeperiod_annotations = self._generate_timperiod_annotations(timeperiods)

        # calculate aggregated actuals (sum, avg, last) per reporting period
        # (monthly, quarterly, tri-annually, seminu-annualy, and yearly) for each indicator
        lastlevel = Level.objects.filter(indicator__id=OuterRef('pk')).order_by('-id')
        last_data_record = CollectedData.objects.filter(indicator=OuterRef('pk')).order_by('-id')
        indicators = Indicator.objects.filter(program__in=[program_id])\
            .annotate(actualsum=Sum('collecteddata__achieved'),
                      actualavg=Avg('collecteddata__achieved'),
                      lastlevel=Subquery(lastlevel.values('name')[:1]),
                      lastdata=Subquery(last_data_record.values('achieved')[:1]),
                      mincollected_date=Min('collecteddata__date_collected'),
                      maxcollected_date=Max('collecteddata__date_collected'))\
            .values('id', 'number', 'name', 'program', 'lastlevel', 'unit_of_measure', 'direction_of_change',
                    'unit_of_measure_type', 'is_cumulative', 'baseline', 'lop_target', 'actualsum', 'actualavg',
                    'lastdata')\
            .annotate(**timeperiod_annotations)\
            .order_by('number', 'name')

        context['start_date'] = start_date
        context['end_date'] = end_date
        context['timeperiods'] = timeperiods
        context['indicators'] = indicators
        context['program'] = program
        context['reporttype'] = kwargs.get('reporttype')
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        pass
