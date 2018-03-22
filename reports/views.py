from django.views.generic import TemplateView, View
from workflow.models import WorkflowLevel2, WorkflowLevel1
from indicators.models import CollectedData, Indicator
from .forms import FilterForm

from django.db.models import Q
from django.http import HttpResponse, JsonResponse

import json
import simplejson

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
