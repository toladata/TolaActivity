from dateutil import rrule, relativedelta
from datetime import datetime
from django.core.urlresolvers import reverse_lazy
from django.db.models import Sum, Avg, Subquery, OuterRef, Case, When, Q, F, Min, Max, Count
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
        redirect_url = reverse_lazy('iptt_report', kwargs={'program_id': program.id, 'reporttype': prefix})

        redirect_url = "{}?period={}".format(redirect_url, period)
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
    start_date = None
    end_date = None

    @staticmethod
    def get_num_months(period):
        """
        Returns the number of months for a given time-period
        """
        return {'1': 12, '2': 6, '3': 4, '4': 3, '5': 1}[period]

    def get_period_annotation(self, period):
        num_months_in_period = self.get_num_months(period)
        while self.start_date < self.end_date:
            next_period = self.start_date + relativedelta.relativedelta(months=num_months_in_period)
            yield Sum(Case(When(Q(collecteddata__date_collected__gte=datetime.strftime(self.start_date, '%Y-%m-%d')) &
                                Q(collecteddata__date_collected__lte=datetime.strftime(next_period, '%Y-%m-%d')),
                                then=F('collecteddata__achieved'))))
            self.start_date = next_period


    def get_num_periods(self, start_date, end_date, period):
        """
        Returns the number of periods depending on the period is in terms of months
        """
        num_months_in_period = self.get_num_months(period)
        total_num_months = len(list(rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date)))
        num_periods = total_num_months / num_months_in_period
        remainder_months = total_num_months % num_months_in_period
        if remainder_months > 0:
            num_periods += 1
        return num_periods

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        program_id = kwargs.get('program_id')
        period = request.GET.get('period', None)
        program = Program.objects.get(pk=program_id)

        # determine the full date range of data collection for this program
        data_date_range = Indicator.objects.filter(program__in=[program_id])\
            .aggregate(sdate=Min('collecteddata__date_collected'),
                       edate=Max('collecteddata__date_collected'))
        self.start_date = data_date_range['sdate']
        self.end_date = data_date_range['edate']

        #  find out the total number of periods (quarters, months, years, etc) for this program
        nump = self.get_num_periods(self.start_date, self.end_date, period)

        # handle for generating periodic annotation in the queryset
        annotation_generator = self.get_period_annotation(period)

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
            .annotate(**{"q{}".format(i): next(annotation_generator) for i in range(1, nump)})\
            .order_by('number', 'name')

        context['nump'] = range(1, nump)
        context['indicators'] = indicators
        context['program'] = program
        context['reporttype'] = kwargs.get('reporttype')
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        pass
