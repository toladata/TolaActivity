import json

from django.db.models import Q, Sum, F, When, Case, DecimalField, Value

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import PeriodicTarget, CollectedData

class CollecteddataSerializer(serializers.ModelSerializer):
    cumsum = serializers.SerializerMethodField()

    class Meta:
        model = CollectedData
        fields = ('id', 'program', 'indicator', 'periodic_target', 'achieved',
                  'cumsum', 'date_collected', 'evidence', 'tola_table',
                  'agreement', 'complete', 'site', 'create_date', 'edit_date')

    def get_cumsum(self, obj):
      total_achieved = CollectedData.objects.filter(
                indicator=obj.indicator,
                create_date__lt=obj.create_date)\
            .aggregate(Sum('achieved'))['achieved__sum']

      if total_achieved is None:
            total_achieved = 0
      total_achieved = total_achieved + obj.achieved
      return total_achieved


class PeriodictargetSerializer(serializers.ModelSerializer):
    collecteddata_set = CollecteddataSerializer(many=True, read_only=True)
    collecteddata__achieved__sum = serializers.IntegerField()
    cumulative_sum = serializers.IntegerField()

    class Meta:
        model = PeriodicTarget
        fields = ('id', 'indicator', 'period', 'target', 'start_date',
                  'end_date', 'customsort', 'create_date', 'edit_date',
                  'collecteddata_set', 'collecteddata__achieved__sum',
                  'cumulative_sum')