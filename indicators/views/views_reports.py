from dateutil import rrule
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

    @staticmethod
    def getCase():
            return Sum(Case(When(Q(collecteddata__date_collected__gte='2016-01-01') &
                                 Q(collecteddata__date_collected__lte='2019-04-01'),
                                 then=F('collecteddata__achieved'))))

    @staticmethod
    def getMaxLoopNumber(mind, maxd, period):
            # datetime.strptime('2017-01-01', '%Y-%m-%d')
            # datetime.strptime('2018-02-01', '%Y-%m-%d')
            num_months = len(list(rrule.rrule(rrule.MONTHLY,
                                        dtstart=mind,
                                        until=maxd)))
            num_periods = num_months / period
            if num_months % period > 0:
                num_periods += 1
            return num_periods

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        program_id = kwargs.get('program_id')
        period = request.GET.get('period', None)
        period = int(period) if period is not None else 0
        program = Program.objects.get(pk=program_id)

        value_dict = {
            "collecteddata__date_collected__gte": '2017-01-01',
            "collecteddata__date_collected__lte": '2017-04-01'
        }

        data_date_range = Indicator.objects.filter(program__in=[program_id])\
            .aggregate(maxd=Max('collecteddata__date_collected'),
                       mind=Min('collecteddata__date_collected'))

        print(".............................%s............................" % data_date_range['maxd'] )
        print(".............................%s............................" % data_date_range['mind'] )

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
            .order_by('number', 'name')

        #TODO: calculate aggregated actuals (sum, avg, last) per reporting period
        # (monthly, quarterly, tri-annually, seminu-annualy, and yearly) for each indicator

        inds = Indicator.objects.filter(program__in=[program_id]).prefetch_related('collecteddata_set').values('id', 'collecteddata__achieved')
        for indicator in inds:
            print(indicator)

        context['indicators'] = indicators
        context['program'] = program
        context['reporttype'] = kwargs.get('reporttype')
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        pass
