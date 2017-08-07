from django.views.generic import TemplateView, View
from workflow.models import WorkflowLevel2, WorkflowLevel1
from indicators.models import CollectedData, Indicator
from .forms import FilterForm

from django.db.models import Q
from workflow.mixins import AjaxableResponseMixin
from django.http import HttpResponse, JsonResponse

import json
import simplejson

from workflow.export import ProjectAgreementResource
from workflow.export import ProgramResource
from indicators.export import CollectedDataResource
from indicators.export import IndicatorResource


def make_filter(my_request):
    """
    Build a list of filters for each object
    """
    query_attrs = {}
    query_attrs['workflowlevel1'] = {}
    query_attrs['workflowlevel2'] = {}
    query_attrs['indicator'] = {}
    query_attrs['collecteddata'] = {}
    for param, val in my_request.iteritems():
        if param == 'workflowlevel1':
            query_attrs['workflowlevel1']['id__in'] = val.split(',')
            query_attrs['workflowlevel2']['workflowlevel1__id__in'] = val.split(',')
            query_attrs['indicator']['workflowlevel1__id__in'] = val.split(',')
            query_attrs['collecteddata']['indicator__workflowlevel1__id__in'] = val.split(',')
        elif param == 'sector':
            query_attrs['workflowlevel1']['sector__in'] = val.split(',')
            query_attrs['workflowlevel2']['sector__in'] = val.split(',')
            query_attrs['indicator']['sector__in'] = val.split(',')
            query_attrs['collecteddata']['indicator__sector__in'] = val.split(',')
        elif param == 'country':
            query_attrs['workflowlevel1']['country__id__in'] = val.split(',')
            query_attrs['workflowlevel2']['workflowlevel1__country__id__in'] = val.split(',')
            query_attrs['indicator']['workflowlevel1__country__in'] = val.split(',')
            query_attrs['collecteddata']['workflowlevel1__country__in'] = val.split(',')
        elif param == 'indicator__id':
            query_attrs['indicator']['id'] = val
            query_attrs['collecteddata']['indicator__id'] = val
        elif param == 'approval':
            if val == "new":
                query_attrs['workflowlevel2']['status'] = ""
            else:
                query_attrs['workflowlevel2']['status'] = val
        elif param == 'collecteddata__isnull':
            if val == "True":
                query_attrs['indicator']['collecteddata__isnull'] = True
            else:
                query_attrs['indicator']['collecteddata__isnull'] = False
        elif param == 'export':
            """
            IGNORE EXPORT PARAM
            """
        else:
            query_attrs['workflowlevel1'][param] = val
            query_attrs['workflowlevel2'][param] = val
            query_attrs['indicator'][param] = val
            query_attrs['collecteddata'][param] = val

    return query_attrs


class ReportHome(TemplateView):
    """
    List of available reports
    """
    template_name = 'report.html'

    def get_context_data(self, **kwargs):
        context = super(ReportHome, self).get_context_data(**kwargs)
        form = FilterForm()
        context['form'] = form

        context['criteria'] = json.dumps(kwargs)

        return context


class ReportData(View, AjaxableResponseMixin):
    """
    Main report view
    """
    def get(self, request, *args, **kwargs):

        filter = make_filter(self.request.GET)
        program_filter = filter['workflowlevel1']
        project_filter = filter['workflowlevel2']
        indicator_filter = filter['indicator']

        workflowlevel1 = WorkflowLevel1.objects.all().filter(**program_filter).values('unique_id', 'name', 'funding_status', 'cost_center', 'country__country', 'sector__sector')
        approval_count = WorkflowLevel2.objects.all().filter(**project_filter).filter(status='awaitingapproval').count()
        approved_count = WorkflowLevel2.objects.all().filter(**project_filter).filter(status='tracking').count()
        inprogress_count = WorkflowLevel2.objects.all().filter(**project_filter).filter(status='closed').count()
        nostatus_count = WorkflowLevel2.objects.all().filter(**project_filter).filter(Q(Q(status=None) | Q(status=""))).count()

        indicator_count = Indicator.objects.all().filter(**indicator_filter).filter(collecteddata__isnull=True).count()
        indicator_data_count = Indicator.objects.all().filter(**indicator_filter).filter(collecteddata__isnull=False).count()

        program_serialized = json.dumps(list(workflowlevel1))

        final_dict = {
            'criteria': program_filter, 'workflowlevel1': program_serialized,
            'approval_count': approval_count,
            'approved_count': approved_count,
            'inprogress_count': inprogress_count,
            'nostatus_count': nostatus_count,
            'indicator_count': indicator_count,
            'data_count': indicator_data_count
        }

        if request.GET.get('export'):
            program_export = WorkflowLevel1.objects.all().filter(**program_filter)
            program_dataset = ProgramResource().export(program_export)
            response = HttpResponse(program_dataset.csv, content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=workflowlevel1_data.csv'
            return response

        return JsonResponse(final_dict, safe=False)


class ProjectReportData(View, AjaxableResponseMixin):
    """
    Project based report view
    """
    def get(self, request, *args, **kwargs):
        filter = make_filter(self.request.GET)
        project_filter = filter['workflowlevel2']
        indicator_filter = filter['indicator']

        print project_filter

        project = WorkflowLevel2.objects.all().filter(**project_filter).values('workflowlevel1__name','project_name','activity_code','project_type__name','sector__sector','total_estimated_budget','status')
        approval_count = WorkflowLevel2.objects.all().filter(**project_filter).filter(program__funding_status="Funded", status='awaiting approval').count()
        approved_count = WorkflowLevel2.objects.all().filter(**project_filter).filter(program__funding_status="Funded", status='approved').count()
        rejected_count = WorkflowLevel2.objects.all().filter(**project_filter).filter(program__funding_status="Funded", status='rejected').count()
        inprogress_count = WorkflowLevel2.objects.all().filter(**project_filter).filter(program__funding_status="Funded", status='in progress').count()
        nostatus_count = WorkflowLevel2.objects.all().filter(**project_filter).filter(Q(Q(approval=None) | Q(approval=""))).count()
        indicator_count = Indicator.objects.all().filter(**indicator_filter).filter(collecteddata__isnull=True).count()
        indicator_data_count = Indicator.objects.all().filter(**indicator_filter).filter(collecteddata__isnull=False).count()

        project_serialized = simplejson.dumps(list(project))

        final_dict = {
            'criteria': project_filter, 'project': project_serialized,
            'approval_count': approval_count,
            'approved_count': approved_count,
            'rejected_count': rejected_count,
            'inprogress_count': inprogress_count,
            'nostatus_count': nostatus_count,
            'indicator_count': indicator_count,
            'data_count': indicator_data_count,
        }

        if request.GET.get('export'):
            project_export = WorkflowLevel2.objects.all().filter(**project_filter)
            dataset = ProjectAgreementResource().export(project_export)
            response = HttpResponse(dataset.csv, content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=project_data.csv'
            return response

        return JsonResponse(final_dict, safe=False)


class IndicatorReportData(View, AjaxableResponseMixin):
    """
    Indicator based report view
    """

    def get(self, request, *args, **kwargs):

        filter = make_filter(self.request.GET)
        indicator_filter = filter['indicator']

        indicator = Indicator.objects.all().filter(**indicator_filter).values('id','workflowlevel1__name','workflowlevel1__id','name', 'indicator_type__indicator_type', 'sector__sector','strategic_objectives','level__name','lop_target','collecteddata','key_performance_indicator')
        indicator_count = Indicator.objects.all().filter(**indicator_filter).filter(collecteddata__isnull=True).count()
        indicator_data_count = Indicator.objects.all().filter(**indicator_filter).filter(collecteddata__isnull=False).count()

        indicator_serialized = json.dumps(list(indicator))

        print indicator_filter
        print indicator.query

        final_dict = {
            'criteria': indicator_filter, 'indicator': indicator_serialized,
            'indicator_count': indicator_count,
            'data_count': indicator_data_count
        }

        if request.GET.get('export'):
            indicator_export = Indicator.objects.all().filter(**indicator_filter)
            dataset = IndicatorResource().export(indicator_export)
            response = HttpResponse(dataset.csv, content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=indicator_data.csv'
            return response

        return JsonResponse(final_dict, safe=False)


class CollectedDataReportData(View, AjaxableResponseMixin):
    """
    Indicator based report view
    """

    def get(self, request, *args, **kwargs):

        filter = make_filter(self.request.GET)
        collecteddata_filter = filter['collecteddata']

        collecteddata = CollectedData.objects.all().filter(**collecteddata_filter).values('indicator__workflowlevel1__name','indicator__name','indicator__number','targeted','achieved')

        collecteddata_serialized = json.dumps(list(collecteddata))

        print collecteddata_filter
        print collecteddata.query

        final_dict = {
            'criteria': collecteddata_filter, 'collecteddata': collecteddata_serialized,
        }

        if request.GET.get('export'):
            collecteddata_export = CollectedData.objects.all().filter(**collecteddata_filter)
            dataset = CollectedDataResource().export(collecteddata_export)
            response = HttpResponse(dataset.csv, content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename=collecteddata_data.csv'
            return response

        return JsonResponse(final_dict, safe=False)


def filter_json(request, service, **kwargs):
    """
    For populating indicators in dropdown
    """
    final_dict = {
    'criteria': kwargs}
    print final_dict
    JsonResponse(final_dict, safe=False)