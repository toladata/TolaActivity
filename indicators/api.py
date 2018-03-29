import json
from django.db.models import Q, Sum
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Indicator, PeriodicTarget, CollectedData

class