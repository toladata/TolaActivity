from django.contrib import messages
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic import TemplateView, View
from django.shortcuts import render
from django.contrib import auth
from activitydb.models import ProjectAgreement, ProjectComplete, Program
from .models import Report
from indicators.models import CollectedData, Indicator
from .forms import FilterForm
from util import getCountry
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count
from django.db.models import Q
from activitydb.mixins import AjaxableResponseMixin
from django.http import HttpResponse, JsonResponse

import json

from tola.util import getCountry

from django.contrib.auth.decorators import login_required


def make_filter(my_request):
    """
    Build a list of filters for each object
    """
    query_attrs = {}
    query_attrs['program'] = {}
    query_attrs['project'] = {}
    query_attrs['indicator'] = {}
    for param, val in my_request.iteritems():
        if param == 'program':
            query_attrs['program']['id__in'] = val
            query_attrs['project']['program__id__in'] = val
            query_attrs['indicator']['program__id__in'] = val
        elif param == 'sector':
            query_attrs['program']['sector__in'] = val
            query_attrs['project']['sector__in'] = val
            query_attrs['indicator']['sector__in'] = val
        elif param == 'country':
            query_attrs['program']['country__in'] = val
            query_attrs['project']['program__country__in'] = val
            query_attrs['indicator']['program__country__in'] = val
        else:
            query_attrs['program'][param] = val
            query_attrs['project'][param] = val
            query_attrs['indicator'][param] = val

    return query_attrs


class ReportHome(TemplateView):
    """
    List of available reports
    """
    template_name='report.html'

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
        program_filter = filter['program']
        project_filter = filter['project']
        indicator_filter = filter['indicator']

        print program_filter

        program = Program.objects.all().filter(**program_filter).values('gaitid', 'name','funding_status','cost_center','country__country','sector__sector')
        approval_count = ProjectAgreement.objects.all().filter(**project_filter).filter(program__funding_status="Funded", approval='awaiting approval').count()
        approved_count = ProjectAgreement.objects.all().filter(**project_filter).filter(program__funding_status="Funded", approval='approved').count()
        rejected_count = ProjectAgreement.objects.all().filter(**project_filter).filter(program__funding_status="Funded", approval='rejected').count()
        inprogress_count = ProjectAgreement.objects.all().filter(**project_filter).filter(Q(program__funding_status="Funded") & Q(Q(approval='in progress') | Q(approval=None) | Q(approval=""))).count()

        indicator_count = Indicator.objects.all().filter(**indicator_filter).count()
        indicator_evidence_count = CollectedData.objects.all().filter(**indicator_filter).count()

        program_serialized = json.dumps(list(program))

        final_dict = {
            'criteria': program_filter, 'program': program_serialized,
            'approval_count': approval_count,
            'approved_count': approved_count,
            'rejected_count': rejected_count,
            'inprogress_count': inprogress_count,
            'indicator_count': indicator_count,
            'evidence_count': indicator_evidence_count
        }

        return JsonResponse(final_dict, safe=False)


def filter_json(request, service, **kwargs):
    """
    For populating indicators in dropdown
    """
    final_dict = {
    'criteria': kwargs}
    print final_dict
    JsonResponse(final_dict, safe=False)