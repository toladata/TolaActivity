from django.core.urlresolvers import reverse_lazy
from django.db.models import OuterRef, Sum, Avg, Subquery
from django.views import View
from django.views.generic import TemplateView, FormView
from django.http import HttpResponseRedirect
from workflow.models import Program
from ..models import Indicator, CollectedData
from ..forms import IPTTReportQuickstartForm, IPTTReportFilterForm


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
        prefix = None

        # populate the correct form with POST data
        if targetprefix is not None:
            form = IPTTReportQuickstartForm(self.request.POST,
                                            prefix=self.FORM_PREFIX_TARGET,
                                            request=self.request)
            prefix = targetprefix
        else:
            form = IPTTReportQuickstartForm(self.request.POST,
                                            prefix=self.FORM_PREFIX_TIME,
                                            request=self.request)
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

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        program_id = kwargs.get('program_id')
        program = Program.objects.get(pk=program_id)

        last_data_record = CollectedData.objects.filter(indicator=OuterRef('pk')).order_by('-id')
        indicators = Indicator.objects.filter(program__in=[program_id])\
            .annotate(actualsum=Sum('collecteddata__achieved'),
                      actualavg=Avg('collecteddata__achieved'),
                      lastdata=Subquery(last_data_record.values('achieved')[:1]))

        context['indicators'] = indicators
        context['program'] = program
        context['reporttype'] = kwargs.get('reporttype')
        context['form'] = IPTTReportFilterForm()

        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):

        form = IPTTReportFilterForm(request.POST, request=request)

        if form.is_valid():
            return self.form_valid(form)

        elif not form.is_valid():
            return self.form_invalid(form)

    def form_valid(self, form):
        context = self.get_context_data()
        context['form'] = form

        return self.render_to_response(context=context)

    def form_invalid(self, form):

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context=context)



