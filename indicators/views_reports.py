
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import View
from django.views.generic import TemplateView, FormView
from .models import Indicator, PeriodicTarget, CollectedData
from .forms import IPTTReportQuickstartForm

class IPTTReportQuickstartView(FormView):
    template_name = 'indicators/iptt_quickstart.html'
    form_class = IPTTReportQuickstartForm
    second_form_class = IPTTReportQuickstartForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super(IPTTReportQuickstartView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(request=self.request,
                                              prefix='timerperiods')
        if 'form2' not in context:
            context['form2'] = self.second_form_class(request=self.request,
                                                      prefix='targetperiods')
        return context

    def form_invalid(self, form):
        print(".............................%s............................" % 'invalid form' )
        print(".............................%s............................" % form.errors.as_json() )
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        print(".............................%s............................" % 'success form' )
        return self.render_to_response(self.get_context_data(form=form))

    def get_form_kwargs(self):
        kwargs = super(IPTTReportQuickstartView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

