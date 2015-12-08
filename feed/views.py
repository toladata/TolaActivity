from .serializers import UserSerializer, ProgramSerializer, SectorSerializer, ProjectTypeSerializer, OfficeSerializer, \
    SiteProfileSerializer, CountrySerializer, AgreementSerializer, CompleteSerializer, ProjectTypeOtherSerializer, IndicatorSerializer, ReportingFrequencySerializer, TolaUserSerializer, IndicatorTypeSerializer, ObjectiveSerializer, DisaggregationTypeSerializer, LevelSerializer

from django.contrib.auth.decorators import login_required
import json as simplejson
from tola.util import siloToDict
from activitydb.models import Program, Sector, ProjectType, Office, SiteProfile, Country, ProjectComplete, ProjectAgreement, ProjectTypeOther
from indicators.models import Indicator, Objective, ReportingFrequency, TolaUser, IndicatorType, DisaggregationType, Level

from django.contrib import messages
from django.template import RequestContext
from django.contrib.auth.models import User

from rest_framework import renderers,viewsets

import operator
import csv

from django.core.urlresolvers import reverse
from django.http import HttpResponseForbidden,\
    HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest,\
    HttpResponse
from django.shortcuts import render_to_response, get_object_or_404, redirect, render


# API Classes
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProgramViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class SectorViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Sector.objects.all()
    serializer_class = SectorSerializer


class ProjectTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer


class OfficeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer


class SiteProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = SiteProfile .objects.all()
    serializer_class = SiteProfileSerializer


class CountryViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class AgreementViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = ProjectAgreement.objects.all()
    serializer_class = AgreementSerializer


class CompleteViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = ProjectComplete.objects.all()
    serializer_class = CompleteSerializer


class ProjectTypeOtherViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = ProjectTypeOther.objects.all()
    serializer_class = ProjectTypeOtherSerializer

class IndicatorViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer

class ReportingFrequencyViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = ReportingFrequency.objects.all()
    serializer_class = ReportingFrequencySerializer

class TolaUserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = TolaUser.objects.all()
    serializer_class = TolaUserSerializer

class IndicatorTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = IndicatorType.objects.all()
    serializer_class = IndicatorTypeSerializer

class ObjectiveViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Objective.objects.all()
    serializer_class = ObjectiveSerializer

class DisaggregationTypeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = DisaggregationType.objects.all()
    serializer_class = DisaggregationTypeSerializer

class LevelViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Level.objects.all()
    serializer_class = LevelSerializer