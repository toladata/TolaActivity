
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.views.generic.detail import View
from django.views.generic import TemplateView, FormView
from .models import Indicator, PeriodicTarget, CollectedData
from .forms import IPTTReportQuickstartForm

class IPTTReportQuickstartView(FormView):
    template_name = 'indicators/iptt_quickstart.html'
    form_class = IPTTReportQuickstartForm
    FORM_PREFIX_TIME = 'timeperiods'
    FORM_PREFIX_TARGET = 'targetperiods'

    def get_context_data(self, **kwargs):
        context = super(IPTTReportQuickstartView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class(request=self.request,
                                              prefix=self.FORM_PREFIX_TIME)
        if 'form2' not in context:
            context['form2'] = self.form_class(request=self.request,
                                               prefix=self.FORM_PREFIX_TARGET)
        return context

    def get_form_kwargs(self):
        kwargs = super(IPTTReportQuickstartView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def post(self, request, *args, **kwargs):
        targetprefix = request.POST.get('%s-formprefix' % self.FORM_PREFIX_TARGET)

        timeprefix = request.POST.get('%s-formprefix' % self.FORM_PREFIX_TIME)
        prefix = None

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
        if form.is_valid():
            return self.form_valid(**{'form': form, 'prefix': prefix })
        else:
            return self.form_invalid(**{'form': form, 'prefix': prefix })


    def form_valid(self, **kwargs):
        context = self.get_context_data()
        form = kwargs.get('form')
        if kwargs.get('prefix') == self.FORM_PREFIX_TARGET:
            context['form2'] = form
            context['form'] = self.form_class(request=self.request,
                                              prefix=self.FORM_PREFIX_TIME)
        else:
            context['form'] = form
            context['form2'] = self.form_class(request=self.request,
                                               prefix=self.FORM_PREFIX_TARGET)
        return self.render_to_response(context)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data()
        form = kwargs.get('form')
        if kwargs.get('prefix') == self.FORM_PREFIX_TARGET:
            context['form2'] = form
            context['form'] = self.form_class(request=self.request,
                                              prefix=self.FORM_PREFIX_TIME)
        else:
            context['form'] = form
            context['form2'] = self.form_class(request=self.request,
                                               prefix=self.FORM_PREFIX_TARGET)
        return self.render_to_response(context)


