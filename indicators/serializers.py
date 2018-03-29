import json

from django.db.models import Q, Sum, F, When, Case, DecimalField, Value

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import PeriodicTarget, CollectedData

class CollecteddataSerializer(serializers.ModelSerializer):

    class Meta:
        model = CollectedData
        fields = ('id', 'program', 'indicator', 'periodic_target', 'achieved',
                  'date_collected', 'evidence', 'tola_table', 'agreement',
                  'complete', 'site', 'create_date', 'edit_date')


class PeriodictargetSerializer(serializers.ModelSerializer):
    collecteddata_set = CollecteddataSerializer(many=True, read_only=True)

    class Meta:
        model = PeriodicTarget
        fields = ('id', 'indicator', 'period', 'target', 'start_date',
                  'end_date', 'customsort', 'create_date', 'edit_date',
                  'collecteddata_set')