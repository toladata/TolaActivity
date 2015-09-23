from django.contrib import admin
from .models import IndicatorType, Indicator, ReportingFrequency, DisaggregationType, DisaggregationLabel, DisaggregationValue, CollectedData, Objective, Level

admin.site.register(IndicatorType)
admin.site.register(Indicator)
admin.site.register(ReportingFrequency)
admin.site.register(DisaggregationType)
admin.site.register(DisaggregationLabel)
admin.site.register(DisaggregationValue)
admin.site.register(CollectedData)
admin.site.register(Objective)
admin.site.register(Level)

