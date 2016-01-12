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
from models import Indicator, DisaggregationLabel, DisaggregationValue, CollectedData, IndicatorType, Level, ExternalServiceRecord, ExternalService, TolaTable
from activitydb.models import Program, ProjectAgreement, SiteProfile, Country, Sector
from djangocosign.models import UserProfile
from indicators.forms import IndicatorForm, CollectedDataForm
from django.shortcuts import render_to_response
from django.contrib import messages
from tola.util import getCountry
from tables import IndicatorTable, IndicatorDataTable
from django_tables2 import RequestConfig
from activitydb.forms import FilterForm
from .forms import IndicatorForm
from django.db.models import Count, Sum
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import View, DetailView
from django.conf import settings
from django.core import serializers
import requests
from activitydb.mixins import AjaxableResponseMixin
from export import IndicatorResource, CollectedDataResource


class IndicatorList(ListView):
    """
    indicator List
    """
    model = Indicator
    template_name = 'indicators/indicator_list.html'

    def get(self, request, *args, **kwargs):

        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(country__in=countries, funding_status="Funded").distinct()

        if int(self.kwargs['pk']) == 0:
            getProgramsIndicator = Program.objects.all().filter(funding_status="Funded", country__in=countries).order_by('name')
            getIndicators = Indicator.objects.select_related().all()
        else:
            getProgramsIndicator = Program.objects.all().filter(id=self.kwargs['pk'])
            getIndicators = Indicator.objects.all().filter(program__id=self.kwargs['pk']).select_related()

        return render(request, self.template_name, {'getIndicators': getIndicators, 'getPrograms': getPrograms, 'getProgramsIndicator': getProgramsIndicator})


def import_indicator(service=1,deserialize=True):
    """
    Import a indicators from a web service (the dig only for now)
    """
    service = ExternalService.objects.get(id=service)
    #hard code the path to the file for now
    #get_json = open(settings.SITE_ROOT + '/fixtures/dig-indicator-feed.json')
    #print service.feed_url
    response = requests.get(service.feed_url)

    if deserialize == True:
        data = json.loads(response.content) # deserialises it
    else:
        #send json data back not deserialized data
        data = response
    #debug the json data string uncomment dump and print
    #data2 = json.dumps(json_data) # json formatted string
    #print data2

    return data


def indicator_create(request, id=0):
    """
    CREATE AN INDICATOR USING A TEMPLATE FIRST
    """
    getIndicatorTypes = IndicatorType.objects.all()
    getCountries = Country.objects.all()
    countries = getCountry(request.user)
    country_id = Country.objects.get(country=countries[0]).id
    getPrograms = Program.objects.all().filter(funding_status="Funded",country__in=countries).distinct()
    getServices = ExternalService.objects.all()
    program_id = id

    if request.method == 'POST':
        #set vars from form and get values from user

        type = IndicatorType.objects.get(indicator_type="custom")
        country = Country.objects.get(id=request.POST['country'])
        program = Program.objects.get(id=request.POST['program'])
        service = request.POST['services']
        level = Level.objects.all()[0]
        node_id = request.POST['service_indicator']
        owner = request.user
        sector = None
        name = None
        source = None
        definition = None
        external_service_record = None

        #import recursive library for substitution
        import re

        print node_id
        #checkfor service indicator and update based on values
        if node_id != None and int(node_id) != 0:
            getImportedIndicators = import_indicator(service)
            for item in getImportedIndicators:
                if item['nid'] == node_id:
                    getSector, created = Sector.objects.get_or_create(sector=item['sector'])
                    sector=getSector
                    getLevel, created = Level.objects.get_or_create(name=item['level'].title())
                    level=getLevel
                    name=item['title']
                    source=item['source']
                    definition=item['definition']
                    #replace HTML tags if they are in the string
                    definition = re.sub("<.*?>", "", definition)
                    getService = ExternalService.objects.get(id=service)
                    full_url = getService.url + "/" + item['nid']
                    external_service_record = ExternalServiceRecord(record_id=item['nid'],external_service=getService,full_url=full_url)
                    external_service_record.save()
                    getType, created = IndicatorType.objects.get_or_create(indicator_type=item['type'].title())
                    type=getType



        #save form
        new_indicator = Indicator(country=country, owner=owner,sector=sector,name=name,source=source,definition=definition, external_service_record=external_service_record)
        new_indicator.save()
        new_indicator.program.add(program)
        new_indicator.indicator_type.add(type)
        new_indicator.level.add(level)

        latest = new_indicator.id

        #redirect to update page
        messages.success(request, 'Success, Basic Indicator Created!')
        redirect_url = '/indicators/indicator_update/' + str(latest)+ '/'
        return HttpResponseRedirect(redirect_url)

    # send the keys and vars from the json data to the template along with submitted feed info and silos for new form
    return render(request, "indicators/indicator_create.html", {'country_id': country_id, 'program_id':int(program_id),'getCountries':getCountries, 'getPrograms': getPrograms,'getIndicatorTypes':getIndicatorTypes, 'getServices': getServices})


class IndicatorCreate(CreateView):
    """
    indicator Form for indicators not using a template or service indicator first
    """
    model = Indicator
    template_name = 'indicators/indicator_form.html'

    #pre-populate parts of the form
    def get_initial(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        initial = {
            'country': user_profile.country,
            'program': self.kwargs['id'],
            'owner': self.request.user,
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
        program = Indicator.objects.all().filter(id=self.kwargs['pk']).values("program__id")
        kwargs['program'] = program
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
        #get external service data if any
        try:
            getExternalServiceRecord = ExternalServiceRecord.objects.all().filter(indicator__id=self.kwargs['pk'])
        except ExternalServiceRecord.DoesNotExist:
            getExternalServiceRecord = None
        context.update({'getExternalServiceRecord': getExternalServiceRecord})

        return context

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(IndicatorUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        program = Indicator.objects.all().filter(id=self.kwargs['pk']).values("program__id")
        kwargs['program'] = program
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


def indicator_report(request, program=0):
    """
    Show LIST of indicators with a filtered search view using django-tables2
    and django-filter
    """
    countries = getCountry(request.user)
    getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries).distinct()

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
    getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries).distinct()
    getIndicators = Indicator.objects.all().filter(program__id=program).select_related().order_by('level', 'number')
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
                                          ).filter(program__id=program).select_related().order_by('level','number')


    # send the keys and vars from the json data to the template along with submitted feed info and silos for new form
    return render(request, "indicators/grid_report.html", {'getIndicators': getIndicators, 'getPrograms': getPrograms, 'getProgram': getProgram, 'form': FilterForm(), 'helper': FilterForm.helper})


def indicator_data_report(request, id=0, program=0):
    """
    Show LIST of indicator based quantitative outputs with a filtered search view using django-tables2
    and django-filter
    """
    countries = getCountry(request.user)
    getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries).distinct()
    getIndicators = Indicator.objects.select_related().filter(country__in=countries)
    indicator_name = None
    program_name = None
    q = None

    #Build query based on filters and search
    if int(id) != 0:
        getSiteProfile = Indicator.objects.all().filter(id=id).select_related()
        q = {
            'indicator__id': id
        }
        indicator_name = Indicator.objects.get(id=id).name
    else:
        getSiteProfile = SiteProfile.objects.all().select_related()
        q = {
            'indicator__country__in': countries,
        }

    if int(program) != 0:
        getSiteProfile = SiteProfile.objects.all().filter(projectagreement__program__id=program).select_related()
        program_name = Program.objects.get(id=program).name
        q = {
            'program__id':program,
            'agreement__program__id': program,
        }
        #redress the indicator list based on program
        getIndicators = Indicator.objects.select_related().filter(program=program)

    if request.method == "GET" and "search" in request.GET:
        """
         fields = ('targeted', 'achieved', 'description', 'indicator', 'agreement', 'complete')
        """
        queryset = CollectedData.objects.filter(**q).filter(
                                           Q(agreement__project_name__contains=request.GET["search"]) |
                                           Q(description__icontains=request.GET["search"]) |
                                           Q(indicator__name__contains=request.GET["search"])
                                          ).select_related()
    else:
        queryset = CollectedData.objects.all().filter(**q).select_related()

    #pass query to table and configure
    table = IndicatorDataTable(queryset)
    table.paginate(page=request.GET.get('page', 1), per_page=20)

    RequestConfig(request).configure(table)

    # send the keys and vars from the json data to the template along with submitted feed info and silos for new form
    return render(request, "indicators/data_report.html", {'getQuantitativeData':queryset,'countries':countries, 'getSiteProfile':getSiteProfile, 'table': table,'getPrograms':getPrograms, 'getIndicators': getIndicators, 'form': FilterForm(), 'helper': FilterForm.helper, 'id': id,'program':program,'indicator_name':indicator_name, 'program_name': program_name})


class CollectedDataList(ListView):
    """
    CollectedData List
    """
    model = CollectedData
    template_name = 'indicators/collecteddata_list.html'

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(ProjectAgreementUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get(self, request, *args, **kwargs):

        countries = getCountry(request.user)
        getPrograms = Program.objects.all().filter(funding_status="Funded", country__in=countries).distinct()
        getIndicators = Indicator.objects.select_related().filter(country__in=countries).exclude(collecteddata__isnull=True)
        getCollectedData = None
        collected_sum = None

        #filter by program or inidcator or both
        if int(self.kwargs['indicator']) != 0:
            getCollectedData = CollectedData.objects.all().filter(indicator__id=self.kwargs['indicator'])
            collected_sum = CollectedData.objects.filter(indicator__id=self.kwargs['indicator']).aggregate(Sum('targeted'),Sum('achieved'))
        elif int(self.kwargs['indicator']) == 0 and int(self.kwargs['program']) != 0:
            getCollectedData = CollectedData.objects.all().filter(program=self.kwargs['program'])
            collected_sum = CollectedData.objects.filter(program=self.kwargs['program']).aggregate(Sum('targeted'),Sum('achieved'))
            #redress indicator query based on submitted program
            getIndicators = Indicator.objects.select_related().filter(program=self.kwargs['program']).exclude(collecteddata__isnull=True)
        elif int(self.kwargs['indicator']) != 0 and int(self.kwargs['program']) != 0:
            getCollectedData = CollectedData.objects.all().filter(program=self.kwargs['program'],indicator__id=self.kwargs['indicator'])
            collected_sum = CollectedData.objects.filter(program=self.kwargs['program'],indicator__id=self.kwargs['indicator']).aggregate(Sum('targeted'),Sum('achieved'))
            #redress indicator query based on submitted program
            getIndicators = Indicator.objects.select_related().filter(program=self.kwargs['program']).exclude(collecteddata__isnull=True)
        elif int(self.kwargs['indicator']) == 0 and int(self.kwargs['program']) == 0:
            getCollectedData = CollectedData.objects.all().filter(indicator__country__in=countries)
            collected_sum = CollectedData.objects.filter(indicator__country__in=countries).aggregate(Sum('targeted'),Sum('achieved'))


        #get details about the filtered indicator or program
        try:
            filter_indicator = Indicator.objects.get(id=self.kwargs['indicator'])
        except Indicator.DoesNotExist:
            filter_indicator = None

        try:
            filter_program = Program.objects.get(id=self.kwargs['program'])
        except Program.DoesNotExist:
            filter_program = None

        #TEMP CODE to migrate inidcators for Afghanistan that do not have programs but have Agreements
        if getCollectedData:
            for data in getCollectedData:
                set_program = None
                if data.program is None and data.agreement:
                    try:
                        program_from_agreement = ProjectAgreement.objects.get(id=data.agreement.id)
                        set_program = program_from_agreement.program
                    except ProjectAgreement.DoesNotExist:
                        set_program = None
                    if set_program:
                        update=CollectedData.objects.filter(id=data.pk).update(program=set_program)

        #END TEMP CODE

        return render(request, self.template_name, {'getCollectedData': getCollectedData, 'getPrograms': getPrograms, 'getIndicators':getIndicators,'filter_program':filter_program,'filter_indicator': filter_indicator, 'collected_sum': collected_sum})


class CollectedDataCreate(CreateView):
    """
    CollectedData Form
    """
    model = CollectedData
    template_name = 'indicators/collecteddata_form.html'
    form_class = CollectedDataForm

    def get_context_data(self, **kwargs):
        context = super(CollectedDataCreate, self).get_context_data(**kwargs)
        try:
            getDisaggregationLabel = DisaggregationLabel.objects.all().filter(disaggregation_type__indicator__id=self.kwargs['indicator'])
        except DisaggregationLabel.DoesNotExist:
            getDisaggregationLabel = None

        #set values to None so the form doesn't display empty fields for previous entries
        getDisaggregationValue = None

        context.update({'getDisaggregationValue': getDisaggregationValue})
        context.update({'getDisaggregationLabel': getDisaggregationLabel})
        context.update({'indicator_id': self.kwargs['indicator']})
        context.update({'program_id': self.kwargs['program']})

        return context

    def get_initial(self):
        initial = {
            'indicator': self.kwargs['indicator'],
            'program': self.kwargs['program'],
        }

        return initial

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(CollectedDataCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['program'] = self.kwargs['program']

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

        redirect_url = '/indicators/home/0/'
        return HttpResponseRedirect(redirect_url)


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
        program = CollectedData.objects.get(id=self.kwargs['pk']).program
        kwargs = super(CollectedDataUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['program'] = program
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
    success_url = '/indicators/collecteddata/0/0/'


def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z


def collecteddata_import(request):
    """
    import collected data from Tola Tables
    """
    owner = request.user
    service = ExternalService.objects.get(name="TolaTables")

    #add filter to get just the users tables only
    user_filter_url = service.feed_url + "&owner__username=" + str(owner)
    #public_filter_url = service.feed_url + "&public=True"
    #shared_filter_url = service.feed_url + "&shared__username=" + str(owner)

    response = requests.get(user_filter_url)
    user_json = json.loads(response.content)

    data = user_json

    #debug the json data string uncomment dump and print
    #data2 = json.dumps(data) # json formatted string
    #print data2

    if request.method == 'POST':
        id = request.POST['service_table']
        filter_url = service.feed_url + "&id=" + id
        response = requests.get(filter_url)
        get_json = json.loads(response.content)
        data = get_json
        for item in data['results']:
            name = item['name']
            url = item['data']
            remote_owner = item['owner']['username']

        check_for_existence = TolaTable.objects.all().filter(name=name,owner=owner)
        if check_for_existence:
            result = "error"
        else:
            create_table = TolaTable.objects.create(name=name,owner=owner,remote_owner=remote_owner,table_id=id,url=url)
            create_table.save()
            result = "success"

        #send result back as json
        message = result
        return HttpResponse(json.dumps(message), content_type='application/json')

    # send the keys and vars from the json data to the template along with submitted feed info and silos for new form
    return render(request, "indicators/collecteddata_import.html", {'getTables': data})


def service_json(request, service):
    """
    For populating service indicators in dropdown
    """
    service_indicators = import_indicator(service,deserialize=False)
    return HttpResponse(service_indicators, content_type="application/json")


def collected_data_json(AjaxableResponseMixin, indicator,program):
    """
    For populating service indicators in dropdown
    """
    template_name = 'indicators/collected_data_table.html'
    collecteddata = CollectedData.objects.all().filter(indicator=indicator)
    collected_sum = CollectedData.objects.filter(indicator=indicator).aggregate(Sum('targeted'),Sum('achieved'))
    return render_to_response(template_name, {'collecteddata': collecteddata, 'collected_sum': collected_sum, 'indicator_id': indicator, 'program_id': program})


def tool(request):

    return render(request, 'indicators/tool.html')


class IndicatorExport(View):
    """
    Export all incidents to a CSV file called from a button at the bottom of the incidentList table
    """

    def get(self, *args, **kwargs ):
        queryset = Indicator.objects.all().filter(program=self.kwargs['program'])
        dataset = IndicatorResource().export(queryset)
        response = HttpResponse(dataset, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=indicator.csv'
        return response


class CollectedDataExport(View):
    """
    Export all incidents to a CSV file called from a button at the bottom of the incidentList table
    """

    def get(self, *args, **kwargs ):
        #filter by program or indicator
        print int(self.kwargs['program'])
        print int(self.kwargs['indicator'])
        if int(self.kwargs['program']) != 0 and int(self.kwargs['indicator']) == 0:
            print "Program"
            queryset = CollectedData.objects.all().filter(indicator__program__id=self.kwargs['program'])
        elif int(self.kwargs['program']) == 0 and int(self.kwargs['indicator']) != 0:
            print "Indicator"
            queryset = CollectedData.objects.all().filter(indicator__id=self.kwargs['indicator'])
        else:
            countries = getCountry(self.request.user)
            queryset = CollectedData.objects.all().filter(indicator__country__in=countries)
        dataset = CollectedDataResource().export(queryset)
        response = HttpResponse(dataset, content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=indicator_data.csv'
        return response