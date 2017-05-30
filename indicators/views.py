from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from urlparse import urlparse
import re
from .models import Indicator, DisaggregationLabel, DisaggregationValue, CollectedData, IndicatorType, Level, ExternalServiceRecord, ExternalService, TolaTable
from workflow.models import WorkflowLevel1, SiteProfile, Country, Sector, TolaSites, TolaUser, FormGuidance
from django.shortcuts import render_to_response
from django.contrib import messages
from tola.util import getCountry, get_table
from tables import IndicatorDataTable
from django_tables2 import RequestConfig
from workflow.forms import FilterForm
from .forms import IndicatorForm, CollectedDataForm

from django.db.models import Count, Sum
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

from workflow.mixins import AjaxableResponseMixin
import json

import requests
from export import IndicatorResource, CollectedDataResource


def group_excluded(*group_names, **url):
    """
    If user is in the group passed in permission denied
    :param group_names:
    :param url:
    :return: Bool True or False is users passes test
    """
    def in_groups(u):
        if u.is_authenticated():
            if not bool(u.groups.filter(name__in=group_names)):
                return True
            raise PermissionDenied
        return False
    return user_passes_test(in_groups)


class IndicatorList(ListView):
    """
    Main Indicator Home Page, displays a list of Indicators Filterable by Program
    """
    model = Indicator
    template_name = 'indicators/indicator_list.html'

    def get(self, request, *args, **kwargs):

        countries = getCountry(request.user)
        getPrograms = WorkflowLevel1.objects.all().filter(funding_status="Funded", country__in=countries).distinct()
        getIndicators = Indicator.objects.all().filter(workflowlevel1__country__in=countries).exclude(collecteddata__isnull=True)
        getIndicatorTypes = IndicatorType.objects.all()
        workflowlevel1 = self.kwargs['workflowlevel1']
        indicator = self.kwargs['indicator']
        type = self.kwargs['type']
        indicator_name = ""
        type_name = ""
        workflowlevel1_name = ""

        q = {'id__isnull': False}
        # if we have a workflowlevel1 filter active
        if int(workflowlevel1) != 0:
            q = {
                'id': workflowlevel1,
            }
            # redress the indicator list based on workflowlevel1
            getIndicators = Indicator.objects.select_related().filter(workflowlevel1=workflowlevel1)
            workflowlevel1_name = WorkflowLevel1.objects.get(id=workflowlevel1)
        # if we have an indicator type active
        if int(type) != 0:
            r = {
                'indicator__indicator_type__id': type,
            }
            q.update(r)
            # redress the indicator list based on type
            getIndicators = Indicator.objects.select_related().filter(indicator_type__id=type)
            type_name = IndicatorType.objects.get(id=type).indicator_type
        # if we have an indicator id append it to the query filter
        if int(indicator) != 0:
            s = {
                'indicator': indicator,
            }
            q.update(s)
            indicator_name = Indicator.objects.get(id=indicator)

        indicators = WorkflowLevel1.objects.all().filter(funding_status="Funded", country__in=countries).filter(**q).order_by('name').annotate(indicator_count=Count('indicator'))
        return render(request, self.template_name, {'getPrograms': getPrograms,'getIndicators':getIndicators,
                                                    'workflowlevel1_name':workflowlevel1_name, 'indicator_name':indicator_name,
                                                    'type_name':type_name, 'workflowlevel1':workflowlevel1, 'indicator': indicator, 'type': type,
                                                    'getProgramsIndicator': indicators, 'getIndicatorTypes': getIndicatorTypes})


def import_indicator(service=1,deserialize=True):
    """
    Import a indicators from a web service (the dig only for now)
    :param service:
    :param deserialize:
    :return:
    """
    service = ExternalService.objects.get(id=service)
    response = requests.get(service.feed_url)

    if deserialize == True:
        data = json.loads(response.content) # deserialises it
    else:
        # send json data back not deserialized data
        data = response
    #debug the json data string uncomment dump and print
    #data2 = json.dumps(json_data) # json formatted string
    #print data2

    return data


def indicator_create(request, id=0):
    """
    Create an Indicator with a service template first, or custom.  Step one in Inidcator creation.
    Passed on to IndicatorCreate to do the creation
    :param request:
    :param id:
    :return:
    """
    getIndicatorTypes = IndicatorType.objects.all()
    getCountries = Country.objects.all()
    countries = getCountry(request.user)
    country_id = Country.objects.get(country=countries[0]).id
    getPrograms = WorkflowLevel1.objects.all().filter(funding_status="Funded", country__in=countries).distinct()
    getServices = ExternalService.objects.all()
    workflowlevel1_id = id

    if request.method == 'POST':
        #set vars from form and get values from user

        type = IndicatorType.objects.get(indicator_type="custom")
        country = Country.objects.get(id=request.POST['country'])
        workflowlevel1 = WorkflowLevel1.objects.get(id=request.POST['workflowlevel1'])
        service = request.POST['services']
        level = Level.objects.all()[0]
        node_id = request.POST['service_indicator']
        sector = None
        # add a temp name for custom indicators
        name = "Temporary"
        source = None
        definition = None
        external_service_record = None

        #import recursive library for substitution
        import re

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
        new_indicator = Indicator(sector=sector,name=name,source=source,definition=definition, external_service_record=external_service_record)
        new_indicator.save()
        new_indicator.workflowlevel1.add(workflowlevel1)
        new_indicator.indicator_type.add(type)
        new_indicator.level.add(level)

        latest = new_indicator.id

        #redirect to update page
        messages.success(request, 'Success, Basic Indicator Created!')
        redirect_url = '/indicators/indicator_update/' + str(latest)+ '/'
        return HttpResponseRedirect(redirect_url)

    # send the keys and vars from the json data to the template along with submitted feed info and silos for new form
    return render(request, "indicators/indicator_create.html", {'country_id': country_id, 'workflowlevel1_id':int(workflowlevel1_id),'getCountries':getCountries,
                                                                'getPrograms': getPrograms,'getIndicatorTypes':getIndicatorTypes, 'getServices': getServices})


class IndicatorCreate(CreateView):
    """
    Indicator Form for indicators not using a template or service indicator first as well as the post reciever
    for creating an indicator.  Then redirect back to edit view in IndicatorUpdate.
    """
    model = Indicator
    template_name = 'indicators/indicator_form.html'

    #pre-populate parts of the form
    def get_initial(self):
        user_profile = TolaUser.objects.get(user=self.request.user)
        initial = {
            'workflowlevel1': self.kwargs['id'],
            }

        return initial

    def get_context_data(self, **kwargs):
        context = super(IndicatorCreate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['id']})
        return context

    @method_decorator(group_excluded('ViewOnly', url='workflow/permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(IndicatorCreate, self).dispatch(request, *args, **kwargs)

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(IndicatorCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        workflowlevel1 = Indicator.objects.all().filter(id=self.kwargs['pk']).values("workflowlevel1__id")
        kwargs['workflowlevel1'] = workflowlevel1
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
    Update and Edit Indicators.
    """
    model = Indicator
    template_name = 'indicators/indicator_form.html'

    @method_decorator(group_excluded('ViewOnly', url='workflow/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="Indicator")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(IndicatorUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(IndicatorUpdate, self).get_context_data(**kwargs)
        context.update({'id': self.kwargs['pk']})
        getIndicator = Indicator.objects.get(id=self.kwargs['pk'])

        context.update({'i_name': getIndicator.name})

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
        workflowlevel1 = Indicator.objects.all().filter(id=self.kwargs['pk']).values_list("workflowlevel1__id", flat=True)
        kwargs['workflowlevel1'] = workflowlevel1
        return kwargs

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Form', fail_silently=False)
        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):
        form.save()

        messages.success(self.request, 'Success, Indicator Updated!')

        if self.request.POST.has_key('_addanother'):
            url = "/indicators/indicator_create/"
            workflowlevel1 = self.request.POST['workflowlevel1']
            qs = workflowlevel1 + "/"
            return HttpResponseRedirect(''.join((url, qs)))

        return self.render_to_response(self.get_context_data(form=form))

    form_class = IndicatorForm


class IndicatorDelete(DeleteView):
    """
    Delete and Indicator
    """
    model = Indicator
    success_url = '/indicators/home/0/0/0/'

    @method_decorator(group_excluded('ViewOnly', url='workflow/permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(IndicatorDelete, self).dispatch(request, *args, **kwargs)

    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        form.save()

        messages.success(self.request, 'Success, Indicator Deleted!')
        return self.render_to_response(self.get_context_data(form=form))

    form_class = IndicatorForm


class CollectedDataCreate(CreateView):
    """
    CollectedData Form
    """
    model = CollectedData
    template_name = 'indicators/collecteddata_form.html'
    form_class = CollectedDataForm

    @method_decorator(group_excluded('ViewOnly', url='workflow/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="CollectedData")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(CollectedDataCreate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CollectedDataCreate, self).get_context_data(**kwargs)
        try:
            getDisaggregationLabel = DisaggregationLabel.objects.all().filter(disaggregation_type__indicator__id=self.kwargs['indicator'])
            getDisaggregationLabelStandard = DisaggregationLabel.objects.all().filter(disaggregation_type__standard=True)
        except DisaggregationLabel.DoesNotExist:
            getDisaggregationLabelStandard = None
            getDisaggregationLabel = None

        #set values to None so the form doesn't display empty fields for previous entries
        getDisaggregationValue = None

        context.update({'getDisaggregationValue': getDisaggregationValue})
        context.update({'getDisaggregationLabel': getDisaggregationLabel})
        context.update({'getDisaggregationLabelStandard': getDisaggregationLabelStandard})
        context.update({'indicator_id': self.kwargs['indicator']})
        context.update({'workflowlevel1_id': self.kwargs['workflowlevel1']})

        return context

    def get_initial(self):
        initial = {
            'indicator': self.kwargs['indicator'],
            'workflowlevel1': self.kwargs['workflowlevel1'],
        }

        return initial

    # add the request to the kwargs
    def get_form_kwargs(self):
        kwargs = super(CollectedDataCreate, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['workflowlevel1'] = self.kwargs['workflowlevel1']
        kwargs['tola_table'] = None

        return kwargs


    def form_invalid(self, form):

        messages.error(self.request, 'Invalid Form', fail_silently=False)

        return self.render_to_response(self.get_context_data(form=form))

    def form_valid(self, form):

        getDisaggregationLabel = DisaggregationLabel.objects.all().filter(Q(disaggregation_type__indicator__id=self.request.POST['indicator']) | Q(disaggregation_type__standard=True))

        # update the count with the value of Table unique count
        if form.instance.update_count_tola_table and form.instance.tola_table:
            try:
                getTable = TolaTable.objects.get(id=self.request.POST['tola_table'])
            except DisaggregationLabel.DoesNotExist:
                getTable = None
            if getTable:
                count = getTableCount(getTable.url,getTable.table_id)
            else:
                count = 0
            form.instance.achieved = count

        new = form.save()

        #save disagg
        for label in getDisaggregationLabel:
            for key, value in self.request.POST.iteritems():
                if key == label.id:
                    value_to_insert = value
                else:
                    value_to_insert = None
            if value_to_insert:
                insert_disaggregationvalue = DisaggregationValue(dissaggregation_label=label, value=value_to_insert,collecteddata=new)
                insert_disaggregationvalue.save()

        messages.success(self.request, 'Success, Data Created!')

        redirect_url = '/indicators/home/0/0/0/#hidden-' + str(self.kwargs['workflowlevel1'])
        return HttpResponseRedirect(redirect_url)


class CollectedDataUpdate(UpdateView):
    """
    CollectedData Form
    """
    model = CollectedData
    template_name = 'indicators/collecteddata_form.html'

    @method_decorator(group_excluded('ViewOnly', url='workflow/permission'))
    def dispatch(self, request, *args, **kwargs):
        try:
            self.guidance = FormGuidance.objects.get(form="CollectedData")
        except FormGuidance.DoesNotExist:
            self.guidance = None
        return super(CollectedDataUpdate, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CollectedDataUpdate, self).get_context_data(**kwargs)
        #get the indicator_id for the collected data
        getIndicator = CollectedData.objects.get(id=self.kwargs['pk'])

        try:
            getDisaggregationLabel = DisaggregationLabel.objects.all().filter(disaggregation_type__indicator__id=getIndicator.indicator_id)
            getDisaggregationLabelStandard = DisaggregationLabel.objects.all().filter(disaggregation_type__standard=True)
        except DisaggregationLabel.DoesNotExist:
            getDisaggregationLabel = None
            getDisaggregationLabelStandard = None

        try:
            getDisaggregationValue = DisaggregationValue.objects.all().filter(collecteddata=self.kwargs['pk']).exclude(disaggregation_label__disaggregation_type__standard=True)
            getDisaggregationValueStandard = DisaggregationValue.objects.all().filter(collecteddata=self.kwargs['pk']).filter(disaggregation_label__disaggregation_type__standard=True)
        except DisaggregationLabel.DoesNotExist:
            getDisaggregationValue = None
            getDisaggregationValueStandard = None

        context.update({'getDisaggregationLabelStandard': getDisaggregationLabelStandard})
        context.update({'getDisaggregationValueStandard': getDisaggregationValueStandard})
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
        get_data = CollectedData.objects.get(id=self.kwargs['pk'])
        kwargs = super(CollectedDataUpdate, self).get_form_kwargs()
        kwargs['request'] = self.request
        kwargs['workflowlevel1'] = get_data.workflowlevel1
        if get_data.tola_table:
            kwargs['tola_table'] = get_data.tola_table.id
        else:
            kwargs['tola_table'] = None
        return kwargs

    def form_valid(self, form):

        getCollectedData = CollectedData.objects.get(id=self.kwargs['pk'])
        getDisaggregationLabel = DisaggregationLabel.objects.all().filter(Q(disaggregation_type__indicator__id=self.request.POST['indicator']) | Q(disaggregation_type__standard=True)).distinct()

        getIndicator = CollectedData.objects.get(id=self.kwargs['pk'])

        # update the count with the value of Table unique count
        if form.instance.update_count_tola_table and form.instance.tola_table:
            try:
                getTable = TolaTable.objects.get(id=self.request.POST['tola_table'])
            except TolaTable.DoesNotExist:
                getTable = None
            if getTable:
                count = getTableCount(getTable.url,getTable.table_id)
            else:
                count = 0
            form.instance.achieved = count

        # save the form then update manytomany relationships
        form.save()

        # Insert or update disagg values
        for label in getDisaggregationLabel:
            for key, value in self.request.POST.iteritems():
                if key == str(label.id):
                    value_to_insert = value
                    save = getCollectedData.disaggregation_value.create(disaggregation_label=label, value=value_to_insert)
                    getCollectedData.disaggregation_value.add(save.id)

        messages.success(self.request, 'Success, Data Updated!')

        redirect_url = '/indicators/home/0/0/0/#hidden-' + str(getIndicator.workflowlevel1.id)
        return HttpResponseRedirect(redirect_url)

    form_class = CollectedDataForm


class CollectedDataDelete(DeleteView):
    """
    CollectedData Delete
    """
    model = CollectedData
    success_url = '/indicators/home/0/0/0/'

    @method_decorator(group_excluded('ViewOnly', url='workflow/permission'))
    def dispatch(self, request, *args, **kwargs):
        return super(CollectedDataDelete, self).dispatch(request, *args, **kwargs)


def getTableCount(url,table_id):
    """
    Count the number of rowns in a TolaTable
    :param table_id: The TolaTable ID to update count from and return
    :return: count : count of rows from TolaTable
    """
    filter_url = url

    # loop over the result table and count the number of records for actuals
    actual_data = get_table(filter_url)
    count = 0

    if actual_data:
        # check if json data is in the 'data' attribute or at the top level of the JSON object
        try:
            looper = actual_data['data']
        except KeyError:
            looper = actual_data

        for item in looper:
            count = count + 1

    # update with new count
    TolaTable.objects.filter(table_id = table_id).update(unique_count=count)

    return count


def merge_two_dicts(x, y):
    """
    Given two dictionary Items, merge them into a new dict as a shallow copy.
    :param x: Dict 1
    :param y: Dict 2
    :return: Merge of the 2 Dicts
    """
    z = x.copy()
    z.update(y)
    return z


def collecteddata_import(request):
    """
    Import collected data from Tola Tables
    :param request:
    :return:
    """
    owner = request.user
    #get the TolaTables URL and token from the sites object
    service = TolaSites.objects.get(site_id=1)

    # add filter to get just the users tables only
    user_filter_url = service.tola_tables_url + "&owner__username=" + str(owner)
    shared_filter_url = service.tola_tables_url + "&shared__username=" + str(owner)

    user_json = get_table(user_filter_url)
    shared_json = get_table(shared_filter_url)

    if type(shared_json) is not dict:
        data = user_json + shared_json
    else:
        data = user_json

    if request.method == 'POST':
        id = request.POST['service_table']
        filter_url = service.tola_tables_url + "&id=" + id

        data = get_table(filter_url)

        # Get Data Info
        for item in data:
            name = item['name']
            url = item['data']
            remote_owner = item['owner']['username']

        #send table ID to count items in data
        count = getTableCount(url,id)

        # get the users country
        countries = getCountry(request.user)
        check_for_existence = TolaTable.objects.all().filter(name=name,owner=owner)
        if check_for_existence:
            result = "error"
        else:
            create_table = TolaTable.objects.create(name=name,owner=owner,remote_owner=remote_owner,table_id=id,url=url, unique_count=count)
            create_table.country.add(countries[0].id)
            create_table.save()
            result = "success"

        # send result back as json
        message = result
        return HttpResponse(json.dumps(message), content_type='application/json')

    # send the keys and vars from the json data to the template along with submitted feed info and silos for new form
    return render(request, "indicators/collecteddata_import.html", {'getTables': data})


def service_json(request,service):
    """
    For populating service indicators in dropdown
    :param service: The remote data service
    :return: JSON object of the indicators from the service
    """
    service_indicators = import_indicator(service,deserialize=False)
    return HttpResponse(service_indicators, content_type="application/json")


def collected_data_json(AjaxableResponseMixin, indicator,workflowlevel1):
    """
    Displayed on the Indicator home page as a table of collected data entries related to an indicator
    Called from Indicator "data" button onClick
    :param AjaxableResponseMixin:
    :param indicator:
    :param workflowlevel1:
    :return: List of CollectedData entries and sum of there achieved & Targets as well as related indicator and workflowlevel1
    """

    template_name = 'indicators/collected_data_table.html'
    collecteddata = CollectedData.objects.all().filter(indicator=indicator).prefetch_related('evidence')

    detail_url = ''
    try:
        for data in collecteddata:
            if data.tola_table:
                data.tola_table.detail_url = const_table_det_url(str(data.tola_table.url))
    except Exception, e:
        # FIXME
        pass

    collected_sum = CollectedData.objects.filter(indicator=indicator).aggregate(Sum('targeted'),Sum('achieved'))
    return render_to_response(template_name, {'collecteddata': collecteddata, 'collected_sum': collected_sum,
                                              'indicator_id': indicator, 'workflowlevel1_id': workflowlevel1})


def workflowlevel1_indicators_json(AjaxableResponseMixin,workflowlevel1,indicator,type):
    """
    Displayed on the Indicator home page as a table of indicators related to a Program
    Called from Program "Indicator" button onClick
    :param AjaxableResponseMixin:
    :param workflowlevel1:
    :return: List of Indicators and the Program they are related to
    """
    template_name = 'indicators/workflowlevel1_indicators_table.html'

    q = {'workflowlevel1__id__isnull': False}
    # if we have a workflowlevel1 filter active
    if int(workflowlevel1) != 0:
        q = {
            'workflowlevel1__id': workflowlevel1,
        }
    # if we have an indicator type active
    if int(type) != 0:
        r = {
            'indicator_type__id': type,
        }
        q.update(r)
    # if we have an indicator id append it to the query filter
    if int(indicator) != 0:
        s = {
            'id': indicator,
        }
        q.update(s)

    indicators = Indicator.objects.all().filter(**q).annotate(data_count=Count('collecteddata'))
    return render_to_response(template_name, {'indicators': indicators, 'workflowlevel1_id': workflowlevel1})


def tool(request):
    """
    Placeholder for Indicator planning Tool TBD
    :param request:
    :return:
    """
    return render(request, 'indicators/tool.html')


# REPORT VIEWS
def indicator_report(request, workflowlevel1=0, indicator=0, type=0):
    """
    This is the indicator library report.  List of all indicators across a country or countries filtered by
    workflowlevel1.  Lives in the "Report" navigation.
    URL: indicators/report/0/
    :param request:
    :param workflowlevel1:
    :return:
    """
    countries = getCountry(request.user)
    getPrograms = WorkflowLevel1.objects.all().filter(funding_status="Funded", country__in=countries).distinct()

    getIndicators = []

    if workflowlevel1 != 0:
        getIndicators = Indicator.objects.filter(workflowlevel1__id= workflowlevel1)

    getIndicatorTypes = IndicatorType.objects.all()

    # send the keys and vars from the json data to the template along with submitted feed info and silos for new form
    return render(request, "indicators/report.html",
                  {'workflowlevel1': workflowlevel1, 'getPrograms': getPrograms, 'form': FilterForm(), 'helper': FilterForm.helper,
                   'getIndicatorTypes': getIndicatorTypes, 'getIndicators': getIndicators})


class IndicatorReport(View, AjaxableResponseMixin):
    def get(self, request, *args, **kwargs):

        countries = getCountry(request.user)
        getPrograms = WorkflowLevel1.objects.all().filter(funding_status="Funded", country__in=countries).distinct()

        getIndicatorTypes = IndicatorType.objects.all()

        workflowlevel1 = int(self.kwargs['workflowlevel1'])
        indicator = int(self.kwargs['indicator'])
        type = int(self.kwargs['type'])

        filters = {}
        if workflowlevel1 != 0:
            filters['workflowlevel1__id'] = workflowlevel1
        if type != 0:
            filters['indicator_type'] = type
        if indicator != 0:
            filters['id'] = indicator
        if workflowlevel1 == 0 and type == 0:
            filters['workflowlevel1__country__in'] = countries

        getIndicators = Indicator.objects.filter(**filters).select_related(\
            'workflowlevel1', 'external_service_record','indicator_type', 'sector', \
            'disaggregation', 'reporting_frequency').\
            values('id','workflowlevel1__name','baseline','level__name','lop_target',\
                   'workflowlevel1__id','external_service_record__external_service__name',\
                   'key_performance_indicator','name','indicator_type__indicator_type',\
                   'sector__sector','disaggregation__disaggregation_type',\
                   'means_of_verification','data_collection_method',\
                   'reporting_frequency__frequency','create_date','edit_date',\
                   'source','method_of_analysis')


        q = request.GET.get('search', None)
        if q:
            getIndicators = getIndicators.filter(
                Q(indicator_type__indicator_type__contains=q) |
                Q(name__contains=q) |
                Q(number__contains=q) |
                Q(number__contains=q) |
                Q(sector__sector__contains=q) |
                Q(definition__contains=q)
            )

        from django.core.serializers.json import DjangoJSONEncoder

        get_indicators = json.dumps(list(getIndicators), cls=DjangoJSONEncoder)

        return JsonResponse(get_indicators, safe=False)


def WorkflowLevel1IndicatorReport(request, workflowlevel1=0):
    """
    This is the GRID report or indicator plan for a workflowlevel1.  Shows a simple list of indicators sorted by level
    and number. Lives in the "Indicator" home page as a link.
    URL: indicators/workflowlevel1_report/[workflowlevel1_id]/
    :param request:
    :param workflowlevel1:
    :return:
    """
    workflowlevel1 = int(workflowlevel1)
    countries = getCountry(request.user)
    getPrograms = WorkflowLevel1.objects.all().filter(funding_status="Funded", country__in=countries).distinct()
    getIndicators = Indicator.objects.all().filter(workflowlevel1__id=workflowlevel1).select_related().order_by('level', 'number')
    getProgram = WorkflowLevel1.objects.get(id=workflowlevel1)

    getIndicatorTypes = IndicatorType.objects.all()

    if request.method == "GET" and "search" in request.GET:
        # list1 = list()
        # for obj in filtered:
        #    list1.append(obj)
        getIndicators = Indicator.objects.all().filter(
            Q(indicator_type__icontains=request.GET["search"]) |
            Q(name__icontains=request.GET["search"]) |
            Q(number__icontains=request.GET["search"]) |
            Q(definition__startswith=request.GET["search"])
        ).filter(workflowlevel1__id=workflowlevel1).select_related().order_by('level', 'number')

    # send the keys and vars from the json data to the template along with submitted feed info and silos for new form
    return render(request, "indicators/grid_report.html", {'getIndicators': getIndicators, 'getPrograms': getPrograms,
                                                           'getProgram': getProgram, 'form': FilterForm(),
                                                           'helper': FilterForm.helper,
                                                           'getIndicatorTypes': getIndicatorTypes})


def indicator_data_report(request, id=0, workflowlevel1=0, type=0):
    """
    This is the Indicator Visual report for each indicator and workflowlevel1.  Displays a list collected data entries
    and sums it at the bottom.  Lives in the "Reports" navigation.
    URL: indicators/data/[id]/[workflowlevel1]/[type]
    :param request:
    :param id: Indicator ID
    :param workflowlevel1: Program ID
    :param type: Type ID
    :return:
    """
    countries = getCountry(request.user)
    getPrograms = WorkflowLevel1.objects.all().filter(funding_status="Funded", country__in=countries).distinct()
    getIndicators = Indicator.objects.select_related().filter(workflowlevel1__country__in=countries)
    getTypes = IndicatorType.objects.all()
    indicator_name = None
    workflowlevel1_name = None
    type_name = None
    q = {'indicator__id__isnull': False}
    z = None

    # Build query based on filters and search
    if int(id) != 0:
        getSiteProfile = Indicator.objects.all().filter(id=id).select_related()
        indicator_name = Indicator.objects.get(id=id).name
        z = {
            'indicator__id': id
        }
    else:
        getSiteProfile = SiteProfile.objects.all().select_related()
        z = {
            'indicator__workflowlevel1__country__in': countries,
        }

    if int(workflowlevel1) != 0:
        getSiteProfile = SiteProfile.objects.all().filter(projectagreement__workflowlevel1__id=workflowlevel1).select_related()
        workflowlevel1_name = WorkflowLevel1.objects.get(id=workflowlevel1).name
        q = {
            'workflowlevel1__id': workflowlevel1
        }
        # redress the indicator list based on workflowlevel1
        getIndicators = Indicator.objects.select_related().filter(workflowlevel1=workflowlevel1)

    if int(type) != 0:
        type_name = IndicatorType.objects.get(id=type).indicator_type
        q = {
            'indicator__indicator_type__id': type,
        }

    if z:
        q.update(z)

    if request.method == "GET" and "search" in request.GET:
        queryset = CollectedData.objects.filter(**q).filter(
            Q(agreement__project_name__contains=request.GET["search"]) |
            Q(description__icontains=request.GET["search"]) |
            Q(indicator__name__contains=request.GET["search"])
        ).select_related()
    else:

        queryset = CollectedData.objects.all().filter(**q).select_related()

    # pass query to table and configure
    table = IndicatorDataTable(queryset)
    table.paginate(page=request.GET.get('page', 1), per_page=20)

    RequestConfig(request).configure(table)

    # send the keys and vars from the json data to the template along with submitted feed info and silos for new form
    return render(request, "indicators/data_report.html",
                  {'getQuantitativeData': queryset, 'countries': countries, 'getSiteProfile': getSiteProfile,
                   'getPrograms': getPrograms, 'getIndicators': getIndicators,
                   'getTypes': getTypes, 'form': FilterForm(), 'helper': FilterForm.helper,
                   'id': id, 'workflowlevel1': workflowlevel1, 'type': type, 'indicator': id, 'indicator_name': indicator_name,
                   'type_name': type_name, 'workflowlevel1_name': workflowlevel1_name})


class IndicatorReportData(View, AjaxableResponseMixin):
    """
    This is the Indicator Visual report data, returns a json object of report data to be displayed in the table report
    URL: indicators/report_data/[id]/[workflowlevel1]/
    :param request:
    :param id: Indicator ID
    :param workflowlevel1: Program ID
    :param type: Type ID
    :return: json dataset
    """

    def get(self, request, workflowlevel1, type, id):
        q = {'workflowlevel1__id__isnull': False}
        # if we have a workflowlevel1 filter active
        if int(workflowlevel1) != 0:
            q = {
                'workflowlevel1__id': workflowlevel1,
            }
        # if we have an indicator type active
        if int(type) != 0:
            r = {
                'indicator_type__id': type,
            }
            q.update(r)
        # if we have an indicator id append it to the query filter
        if int(id) != 0:
            s = {
                'id': id,
            }
            q.update(s)

        countries = getCountry(request.user)

        indicator = Indicator.objects.filter(workflowlevel1__country__in=countries).filter(**q).values('id', 'workflowlevel1__name', 'baseline','level__name','lop_target','workflowlevel1__id','external_service_record__external_service__name', 'key_performance_indicator','name','indicator_type__indicator_type','sector__sector').order_by('create_date')

        #indicator = {x['id']:x for x in indcator}.values()

        indicator_count = Indicator.objects.all().filter(workflowlevel1__country__in=countries).filter(**q).filter(
            collecteddata__isnull=True).distinct().count()
        indicator_data_count = Indicator.objects.all().filter(workflowlevel1__country__in=countries).filter(**q).filter(collecteddata__isnull=False).distinct().count()

        indicator_serialized = json.dumps(list(indicator))

        final_dict = {
            'indicator': indicator_serialized,
            'indicator_count': indicator_count,
            'data_count': indicator_data_count
        }

        if request.GET.get('export'):
            indicator_export = Indicator.objects.all().filter(**q)
            dataset = IndicatorResource().export(indicator_export)
            response = HttpResponse(dataset.csv, content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=indicator_data.csv'
            return response

        return JsonResponse(final_dict, safe=False)


class CollectedDataReportData(View, AjaxableResponseMixin):
    """
    This is the Collected Data reports data in JSON format for a specific indicator
    URL: indicators/collectedaata/[id]/
    :param request:
    :param indicator: Indicator ID
    :return: json dataset
    """

    def get(self, request, *args, **kwargs):

        countries = getCountry(request.user)
        workflowlevel1 = kwargs['workflowlevel1']
        indicator = kwargs['indicator']
        type = kwargs['type']

        q = {'workflowlevel1__id__isnull': False}
        # if we have a workflowlevel1 filter active
        if int(workflowlevel1) != 0:
            q = {
                'indicator__workflowlevel1__id': workflowlevel1,
            }
        # if we have an indicator type active
        if int(type) != 0:
            r = {
                'indicator__indicator_type__id': type,
            }
            q.update(r)
        # if we have an indicator id append it to the query filter
        if int(indicator) != 0:
            s = {
                'indicator__id': indicator,
            }
            q.update(s)

        getCollectedData = CollectedData.objects.all().prefetch_related('evidence', 'indicator', 'workflowlevel1',
                                                                        'indicator__objectives',
                                                                        'indicator__strategic_objectives').filter(
            workflowlevel1__country__in=countries).filter(
            **q).order_by(
            'indicator__workflowlevel1__name',
            'indicator__number').values('id', 'indicator__id', 'indicator__name', 'indicator__workflowlevel1__name',
                                        'indicator__indicator_type__indicator_type', 'indicator__level__name',
                                        'indicator__sector__sector', 'date_collected', 'indicator__baseline',
                                        'indicator__lop_target', 'indicator__key_performance_indicator',
                                        'indicator__external_service_record__external_service__name', 'evidence',
                                        'tola_table', 'targeted', 'achieved')

        #getCollectedData = {x['id']:x for x in getCollectedData}.values()

        collected_sum = CollectedData.objects.filter(workflowlevel1__country__in=countries).filter(**q).aggregate(
            Sum('targeted'), Sum('achieved'))

        # datetime encoding breaks without using this
        from django.core.serializers.json import DjangoJSONEncoder
        collected_serialized = json.dumps(list(getCollectedData), cls=DjangoJSONEncoder)

        final_dict = {
            'collected': collected_serialized,
            'collected_sum': collected_sum
        }

        return JsonResponse(final_dict, safe=False)


class CollectedDataList(ListView):
    """
    This is the Indicator CollectedData report for each indicator and workflowlevel1.  Displays a list collected data entries
    and sums it at the bottom.  Lives in the "Reports" navigation.
    URL: indicators/data/[id]/[workflowlevel1]/[type]
    :param request:
    :param indicator: Indicator ID
    :param workflowlevel1: Program ID
    :param type: Type ID
    :return:
    """
    model = CollectedData
    template_name = 'indicators/collecteddata_list.html'

    def get(self, request, *args, **kwargs):

        countries = getCountry(request.user)
        getPrograms = WorkflowLevel1.objects.all().filter(funding_status="Funded", country__in=countries).distinct()
        getIndicators = Indicator.objects.all().filter(level1__country__in=countries).exclude(
            collecteddata__isnull=True)
        getIndicatorTypes = IndicatorType.objects.all()
        workflowlevel1 = self.kwargs['workflowlevel1']
        indicator = self.kwargs['indicator']
        type = self.kwargs['type']
        indicator_name = ""
        type_name = ""
        workflowlevel1_name = ""

        q = {'workflowlevel1__id__isnull': False}
        # if we have a workflowlevel1 filter active
        if int(workflowlevel1) != 0:
            q = {
                'workflowlevel1__id': workflowlevel1,
            }
            # redress the indicator list based on workflowlevel1
            getIndicators = Indicator.objects.select_related().filter(workflowlevel1=workflowlevel1)
            workflowlevel1_name = WorkflowLevel1.objects.get(id=workflowlevel1)
        # if we have an indicator type active
        if int(type) != 0:
            r = {
                'indicator__indicator_type__id': type,
            }
            q.update(r)
            # redress the indicator list based on type
            getIndicators = Indicator.objects.select_related().filter(indicator_type__id=type)
            type_name = IndicatorType.objects.get(id=type).indicator_type
        # if we have an indicator id append it to the query filter
        if int(indicator) != 0:
            s = {
                'indicator': indicator,
            }
            q.update(s)
            indicator_name = Indicator.objects.get(id=indicator)

        indicators = CollectedData.objects.all().prefetch_related('evidence', 'indicator', 'workflowlevel1',
                                                                  'indicator__objectives',
                                                                  'indicator__strategic_objectives').filter(
            level1__country__in=countries).filter(
            **q).order_by(
            'indicator__workflowlevel1__name',
            'indicator__number').values('indicator__id', 'indicator__name', 'indicator__workflowlevel1__name',
                                        'indicator__indicator_type__indicator_type', 'indicator__level__name',
                                        'indicator__sector__sector', 'date_collected', 'indicator__baseline',
                                        'indicator__lop_target', 'indicator__key_performance_indicator',
                                        'indicator__external_service_record__external_service__name', 'evidence',
                                        'tola_table', 'targeted', 'achieved')

        if self.request.GET.get('export'):
            dataset = CollectedDataResource().export(indicators)
            response = HttpResponse(dataset.csv, content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=indicator_data.csv'
            return response

        return render(request, self.template_name, {'indicators': indicators, 'getPrograms': getPrograms,
                                                    'getIndicatorTypes': getIndicatorTypes,
                                                    'getIndicators': getIndicators,
                                                    'workflowlevel1': workflowlevel1, 'indicator': indicator, 'type': type,
                                                    'filter_workflowlevel1': workflowlevel1_name, 'filter_indicator': indicator_name,
                                                    'indicator': indicator, 'workflowlevel1': workflowlevel1, 'type': type,
                                                    'indicator_name': indicator_name,
                                                    'workflowlevel1_name': workflowlevel1_name, 'type_name': type_name})


class IndicatorExport(View):
    """
    Export all indicators to a CSV file
    """
    def get(self, request, *args, **kwargs ):


        if int(kwargs['id']) == 0:
            del kwargs['id']
        if int(kwargs['indicator_type']) == 0:
            del kwargs['indicator_type']
        if int(kwargs['workflowlevel1']) == 0:
            del kwargs['workflowlevel1']

        countries = getCountry(request.user)

        queryset = Indicator.objects.filter(**kwargs).filter(workflowlevel1__country__in=countries)


        indicator = IndicatorResource().export(queryset)
        response = HttpResponse(indicator.csv, content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=indicator.csv'
        return response


class IndicatorDataExport(View):
    """
    Export all indicators to a CSV file
    """
    def get(self, request, *args, **kwargs ):

        if int(kwargs['indicator']) == 0:
            del kwargs['indicator']
        if int(kwargs['workflowlevel1']) == 0:
            del kwargs['workflowlevel1']
        if int(kwargs['type']) == 0:
            del kwargs['type']
        else:
           kwargs['indicator__indicator_type__id'] = kwargs['type']
           del kwargs['type']

        countries = getCountry(request.user)

        queryset = CollectedData.objects.filter(**kwargs).filter(indicator__workflowlevel1__country__in=countries)
        dataset = CollectedDataResource().export(queryset)
        response = HttpResponse(dataset.csv, content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=indicator_data.csv'
        return response


class CountryExport(View):

    def get(self, *args, **kwargs ):
        country = CountryResource().export()
        response = HttpResponse(country.csv, content_type="csv")
        response['Content-Disposition'] = 'attachment; filename=country.csv'
        return response

def const_table_det_url(url):
    url_data = urlparse(url)
    root = url_data.scheme
    org_host = url_data.netloc
    path = url_data.path
    components = re.split('/', path)

    s = []
    for c in components:
        s.append(c)

    new_url = str(root)+'://'+str(org_host)+'/silo_detail/'+str(s[3])+'/'

    return new_url