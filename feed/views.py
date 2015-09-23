from .serializers import UserSerializer, ProposalSerializer, ProgramSerializer, SectorSerializer, ProjectTypeSerializer, OfficeSerializer, CommunitySerializer, CountrySerializer, AgreementSerializer, CompleteSerializer, ProjectTypeOtherSerializer

from django.contrib.auth.decorators import login_required
import json as simplejson
from tola.util import siloToDict
from activitydb.models import ProjectProposal, Program, Sector, ProjectType, Office, Community, Country, ProjectComplete, ProjectAgreement, ProjectTypeOther

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


class ProposalViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = ProjectProposal.objects.all()
    serializer_class = ProposalSerializer


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


class CommunityViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer


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