from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template import Context, loader
from datetime import date
import os
import urllib2
import json
import unicodedata
from django.http import HttpResponseRedirect
from django.db import models
from models import Indicator, DisaggregationLabel, DisaggregationValue, CollectedData
from activitydb.models import Program, ProjectAgreement, Community
from djangocosign.models import UserProfile
from indicators.forms import IndicatorForm, CollectedDataForm
from django.shortcuts import render_to_response
from django.contrib import messages
from tola.util import getCountry
from tables import IndicatorTable, IndicatorDataTable
from django_tables2 import RequestConfig
from activitydb.forms import FilterForm
from .forms import IndicatorForm
from django.db.models import Count
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import View, DetailView


class IndicatorList(ListView):
    """
    indicator List
    """
    model = Indicator
    template_name = 'indicators/indicator_list.html'

    def get(self, request, *args, **kwargs):

        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(country__in=countries, funding_status="Funded")

        if int(self.kwargs['pk']) == 0:
            getProgramsIndicator = Program.objects.all().filter(funding_status="Funded", country__in=countries)
            getIndicators = Indicator.objects.select_related().all()
        else:
            getProgramsIndicator = Program.objects.all().filter(id=self.kwargs['pk'])
            getIndicators = Indicator.objects.all().filter(program__id=self.kwargs['pk']).select_related()

        return render(request, self.template_name, {'getIndicators': getIndicators, 'getPrograms': getPrograms, 'getProgramsIndicator': getProgramsIndicator})


class IndicatorCreate(CreateView):
    """
    indicator Form
    """
    model = Indicator
    template_name = 'indicators/indicator_form.html'

    #pre-populate parts of the form
    def get_initial(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        initial = {
            'country': user_profile.country,
            }

        return initial

    def get_context_data(self, **kwargs):
        context = super(IndicatorCreate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['id']})
        return context

    def dispatch(self, request, *args, **kwargs):
        return super(IndicatorCreate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(IndicatorCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Indicator Created!')
        form = ""
        return self.render_to_response(self.get_context_data(form=form))


    form_class = IndicatorForm


class IndicatorUpdate(UpdateView):
    """
    indicator Form
    """
    model = Indicator
    template_name = 'indicators/indicator_form.html'


    def get_context_data(self, **kwargs):
        context = super(IndicatorUpdate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(IndicatorUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Success, Indicator Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = IndicatorForm


class IndicatorDelete(DeleteView):
    """
    indicator Delete
    """
    model = Indicator
    success_url = '/'

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Data Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = IndicatorForm


def indicatorReport(request, program=0):
    """
    Show LIST of indicators with a filtered search view using django-tables2
    and django-filter
    """
    countries = getCountry(request.user)
    getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)

    if int(program) == 0:
        getIndicators = Indicator.objects.all().select_related().filter(country__in=countries)
    else:
        getIndicators = Indicator.objects.all().filter(program__id=program).select_related()

    table = IndicatorTable(getIndicators)
    table.paginate(page=request.GET.get('page', 1), per_page=20)

    if request.method == "GET" and "search" in request.GET:
        #list1 = list()
        #for obj in filtered:
        #    list1.append(obj)
        """
         fields = (indicator_type, name, number, source, definition, disaggregation, baseline, lop_target, means_of_verification, data_collection_method, responsible_person,
                    method_of_analysis, information_use, reporting_frequency, comments, program, sector, approved_by, approval_submitted_by, create_date, edit_date)
        """
        queryset = Indicator.objects.filter(
                                           Q(indicator_type__indicator_type__contains=request.GET["search"]) |
                                           Q(name__contains=request.GET["search"]) | Q(number__contains=request.GET["search"]) |
                                           Q(number__contains=request.GET["search"]) | Q(sector__sector__contains=request.GET["search"]) |
                                           Q(definition__contains=request.GET["search"])
                                          )
        table = IndicatorTable(queryset)

    RequestConfig(request).configure(table)

    # send the keys and vars from the json data to the template along with submitted feed info and silos for new form
    return render(request, "indicators/report.html", {'get_agreements': table, 'getPrograms': getPrograms, 'form': FilterForm(), 'helper': FilterForm.helper})


def programIndicatorReport(request, program=0):
    """
    Show LIST of indicators with a filtered search view using django-tables2
    and django-filter
    """
    program = int(program)
    countries = getCountry(request.user)
    getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)
    getIndicators = Indicator.objects.all().filter(program__id=program).select_related().order_by('indicator_type', 'number')
    getProgram = Program.objects.get(id=program)

    if request.method == "GET" and "search" in request.GET:
        #list1 = list()
        #for obj in filtered:
        #    list1.append(obj)
        """
         fields = (indicator_type, name, number, source, definition, disaggregation, baseline, lop_target, means_of_verification, data_collection_method, responsible_person,
                    method_of_analysis, information_use, reporting_frequency, comments, program, sector, approved_by, approval_submitted_by, create_date, edit_date)
        """
        getIndicators = Indicator.objects.all().filter(
                                           Q(indicator_type__icontains=request.GET["search"]) |
                                           Q(name__icontains=request.GET["search"]) |
                                           Q(number__icontains=request.GET["search"]) |
                                           Q(definition__startswith=request.GET["search"])
                                          ).filter(program__id=program).select_related().order_by('indicator_type','number')


    # send the keys and vars from the json data to the template along with submitted feed info and silos for new form
    return render(request, "indicators/grid_report.html", {'getIndicators': getIndicators, 'getPrograms': getPrograms, 'getProgram': getProgram, 'form': FilterForm(), 'helper': FilterForm.helper})


def indicatorDataReport(request, id=0, program=0, agreement=0):
    """
    Show LIST of indicator based quantitative outputs with a filtered search view using django-tables2
    and django-filter
    """
    countries = getCountry(request.user)
    getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries)
    getAgreements = ProjectAgreement.objects.all().filter(country__in=countries)
    getIndicators = Indicator.objects.select_related().filter(country__in=countries)

    if int(id) != 0:
        getQuantitativeData = CollectedData.objects.all().filter(indicator__id=id).select_related()
        getCommunity = CollectedData.objects.all().filter(indicator__id=id).select_related()
    else:
        getQuantitativeData = CollectedData.objects.all().select_related().filter(indicator__country__in=countries)
        getCommunity = Community.objects.all().select_related()

    if int(program) != 0:
        getQuantitativeData = CollectedData.objects.all().filter(agreement__program__id=program).select_related()
        getCommunity = Community.objects.all().filter(projectagreement__program__id=program).select_related()

    if int(agreement) != 0:
        getQuantitativeData = CollectedData.objects.all().filter(agreement__id=agreement).select_related()
        getCommunity = Community.objects.all().filter(projectagreement__id=agreement).select_related()

    table = IndicatorDataTable(getQuantitativeData)
    table.paginate(page=request.GET.get('page', 1), per_page=20)

    if request.method == "GET" and "search" in request.GET:
        print "search"
        #list1 = list()
        #for obj in filtered:
        #    list1.append(obj)
        """
         fields = ('targeted', 'achieved', 'description', 'indicator', 'agreement', 'complete')
        """
        queryset = CollectedData.objects.filter(
                                           Q(agreement__project_name__contains=request.GET["search"]) |
                                           Q(description__icontains=request.GET["search"]) |
                                           Q(indicator__name__contains=request.GET["search"])
                                          ).select_related()
        table = IndicatorDataTable(queryset)

    RequestConfig(request).configure(table)

    # send the keys and vars from the json data to the template along with submitted feed info and silos for new form
    return render(request, "indicators/data_report.html", {'getQuantitativeData':getQuantitativeData,'countries':countries, 'getCommunity':getCommunity, 'table': table, 'getAgreements': getAgreements,'getPrograms':getPrograms, 'getIndicators': getIndicators, 'form': FilterForm(), 'helper': FilterForm.helper, 'id': id,'program':program,'agreement':agreement})


class CollectedDataList(ListView):
    """
    CollectedData List
    """
    model = CollectedData
    template_name = 'indicators/collecteddata_list.html'

    def get(self, request, *args, **kwargs):

        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(country__in=countries, funding_status="Funded")

        if int(self.kwargs['pk']) == 0:
            getCollectedData = CollectedData.objects.all().filter(indicator__country__in=countries)
        else:
            getCollectedData = CollectedData.objects.all().filter(indicator__program__id=self.kwargs['pk'])

        return render(request, self.template_name, {'getCollectedData': getCollectedData, 'getPrograms': getPrograms})


class CollectedDataCreate(CreateView):
    """
    CollectedData Form
    """
    model = CollectedData
    template_name = 'indicators/collecteddata_form.html'
    form_class = CollectedDataForm

    def get_context_data(self, **kwargs):
        context = super(CollectedDataCreate, self).get_context_data(**kwargs)
        print self.kwargs['indicator']
        try:
            getDisaggregationLabel = DisaggregationLabel.objects.all().filter(disaggregation_type__indicator__id=self.kwargs['indicator'])
        except DisaggregationLabel.DoesNotExist:
            getDisaggregationLabel = None

        #set values to None so the form doesn't display empty fields for previous entries
        getDisaggregationValue = None

        context.update({'getDisaggregationValue': getDisaggregationValue})
        context.update({'getDisaggregationLabel': getDisaggregationLabel})
        context.update({'indicator_id': self.kwargs['indicator']})
        return context

    def get_initial(self):
        initial = {
            'indicator': self.kwargs['indicator'],
            'agreement': self.kwargs['agreement'],

        }

        return initial

    def dispatch(self, request, *args, **kwargs):
        return super(CollectedDataCreate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(CollectedDataCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        latest = CollectedData.objects.latest('id')
        getCollectedData = CollectedData.objects.get(id=latest.id)
        getDisaggregationLabel = DisaggregationLabel.objects.all().filter(disaggregation_type__indicator__id=self.kwargs['indicator'])

        for label in getDisaggregationLabel:
            for key, value in self.request.POST.iteritems():
                if key == label.id:
                    value_to_insert = value
                else:
                    value_to_insert = None
            if value_to_insert:
                insert_disaggregationvalue = DisaggregationValue(dissaggregation_label=label, value=value_to_insert,collecteddata=getCollectedData)
                insert_disaggregationvalue.save()

        form.save()
        messages.success(self.request, 'Success, Data Created!')

        form = ""
        return self.render_to_response(self.get_context_data(form=form))


class CollectedDataUpdate(UpdateView):
    """
    CollectedData Form
    """
    model = CollectedData
    template_name = 'indicators/collecteddata_form.html'


    def get_context_data(self, **kwargs):
        context = super(CollectedDataUpdate, self).get_context_data(**kwargs)
        #get the indicator_id for the collected data
        getIndicator = CollectedData.objects.get(id=self.kwargs['pk'])
        try:
            getDisaggregationLabel = DisaggregationLabel.objects.all().filter(disaggregation_type__indicator__id=getIndicator.indicator_id)
        except DisaggregationLabel.DoesNotExist:
            getDisaggregationLabel = None

        try:
            getDisaggregationValue = DisaggregationValue.objects.all().filter(collecteddata=self.kwargs['pk'])
        except DisaggregationLabel.DoesNotExist:
            getDisaggregationValue = None

        context.update({'getDisaggregationValue': getDisaggregationValue})
        context.update({'getDisaggregationLabel': getDisaggregationLabel})
        context.update({'id': self.kwargs['pk']})
        context.update({'indicator_id': getIndicator.indicator_id})
        return context

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(CollectedDataUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):

        getCollectedData = CollectedData.objects.get(id=self.kwargs['pk'])
        getDisaggregationLabel = DisaggregationLabel.objects.all().filter(disaggregation_type__indicator__id=self.request.POST['indicator'])

        #save the form then update manytomany relationships
        form.save()

        #Insert or update disagg values
        for label in getDisaggregationLabel:
            for key, value in self.request.POST.iteritems():
                if key == str(label.id):
                    value_to_insert = value
                    save = getCollectedData.disaggregation_value.create(disaggregation_label=label, value=value_to_insert)
                    getCollectedData.disaggregation_value.add(save.id)

        messages.success(self.request, 'Success, Data Updated!')

        return self.render_to_response(self.get_context_data(form=form))

    form_class = CollectedDataForm


class CollectedDataDelete(DeleteView):
    """
    CollectedData Delete
    """
    model = CollectedData
    success_url = '/'

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Data Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = CollectedDataForm


def tool(request):

    return render(request, 'indicators/tool.html')

