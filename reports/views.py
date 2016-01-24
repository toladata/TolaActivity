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
from indicators.models import CollectedData
from .forms import FilterForm
from util import getCountry
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.db.models import Q
from activitydb.mixins import AjaxableResponseMixin
from django.http import HttpResponse, JsonResponse


import json

from tola.util import getCountry

from django.contrib.auth.decorators import login_required


def get_countries(criteria):
    """
    Get a list of countries along with grants grouped by won and lost
    """
    kwargs = prepare_related_donor_fields_to_lookup_fields(criteria, 'grants__')
    countries = Country.objects.filter(**kwargs)

    # get the drilldowns for win_rates per country
    for c in countries:
        programs = Program.object.all().filter(country=c)
    drilldown_series = programs
    return drilldown_series


class ReportHome(TemplateView):
    template_name='report.html'

    def get_context_data(self, **kwargs):
        context = super(ReportHome, self).get_context_data(**kwargs)
        form = FilterForm()
        context['form'] = form

        context['criteria'] = json.dumps(kwargs)

        return context


class ReportData(View, AjaxableResponseMixin):

    def get(self, request, *args, **kwargs):
        print(self.request.GET)

        program = Program.objects.all().filter(**kwargs).values('id', 'gaitid', 'name','funding_status','cost_center','country','sector')

        program_serialized = json.dumps(list(program))

        final_dict = {
            'criteria': kwargs, 'program': program_serialized}
        return JsonResponse(final_dict, safe=False)


def filter_json(request, service, **kwargs):
    """
    For populating service indicators in dropdown
    """
    print request.GET
    print kwagrs
    final_dict = {
    'criteria': kwargs}
    return HttpResponse(final_dict, content_type="application/json")