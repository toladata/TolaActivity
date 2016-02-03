from django.contrib import admin
from .models import IndicatorType, Indicator, ReportingFrequency, DisaggregationType, DisaggregationLabel,\
    CollectedData, Objective, Level, IndicatorAdmin, ObjectiveAdmin, StrategicObjective, StrategicObjectiveAdmin, ExternalService, \
    ExternalServiceAdmin, ExternalServiceRecord, ExternalServiceRecordAdmin, CollectedDataAdmin
from activitydb.models import Sector, Country, Program
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from import_export.admin import ImportExportModelAdmin


class IndicatorResource(resources.ModelResource):

    country = fields.Field(column_name='country', attribute='country', widget=ForeignKeyWidget(Country, 'country'))
    indicator_type = ManyToManyWidget(IndicatorType, separator=" | ", field="indicator_type")
    objective = ManyToManyWidget(Objective, separator=" | ", field="objective")
    strategic_objective = ManyToManyWidget(StrategicObjective, separator=" | ", field="strategic_objective")
    level = ManyToManyWidget(Level, separator=" | ", field="level")
    reporting_frequency = fields.Field(column_name='reporting_frequency', attribute='reporting_frequency', widget=ForeignKeyWidget(ReportingFrequency, 'frequency'))
    sector = fields.Field(column_name='sector', attribute='sector', widget=ForeignKeyWidget(Sector, 'sector'))
    program = ManyToManyWidget(Program, separator=" | ", field="name")


    class Meta:
        model = Indicator
        fields = ('id','country','indicator_type','level','objective','strategic_objective','name','number',\
                  'source','definition','baseline','lop_target','means_of_verification','data_collection_method','responsible_person',\
                  'method_of_analysis','information_use','reporting_frequency','comments','disaggregation','sector','program','key_performance_indicator')
        #import_id_fields = ['id']


class IndicatorAdmin(ImportExportModelAdmin):
    resource_class = IndicatorResource
    list_display = ('owner','indicator_types','name','sector')
    search_fields = ('name','number','program__name')
    list_filter = ('country','sector')
    display = 'Indicators'
    pass


admin.site.register(IndicatorType)
admin.site.register(Indicator,IndicatorAdmin)
admin.site.register(ReportingFrequency)
admin.site.register(DisaggregationType)
admin.site.register(DisaggregationLabel)
admin.site.register(CollectedData, CollectedDataAdmin)
admin.site.register(Objective,ObjectiveAdmin)
admin.site.register(StrategicObjective, StrategicObjectiveAdmin)
admin.site.register(Level)
admin.site.register(ExternalService, ExternalServiceAdmin)
admin.site.register(ExternalServiceRecord, ExternalServiceRecordAdmin)


