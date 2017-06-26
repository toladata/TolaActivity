import django_tables2 as tables
from indicators.models import Indicator, CollectedData
from django_tables2.utils import A

class IndicatorDataTable(tables.Table):

    indicator__name = tables.LinkColumn('indicator_data_report', args=[A('indicator__id')])

    class Meta:
        model = CollectedData
        attrs = {"class": "paleblue"}
        fields = ('indicator__lop_target', 'actuals','indicator__program__name', 'indicator__number', 'indicator__name')
        sequence = ('indicator__lop_target', 'actuals', 'indicator__program__name','indicator__number', 'indicator__name')


class CollectedDataTable(tables.Table):

    agreement = tables.LinkColumn('projectagreement_update', args=[A('agreement_id')])

    class Meta:
        model = CollectedData
        attrs = {"class": "paleblue"}
        fields = ('targeted', 'achieved', 'description', 'logframe_indicator', 'sector', 'community', 'agreement', 'complete')
        sequence = ('targeted', 'achieved', 'description', 'logframe_indicator', 'sector', 'community', 'agreement', 'complete')