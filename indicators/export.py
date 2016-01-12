from import_export import resources
from .models import Indicator, CollectedData, Country, IndicatorType, Objective, StrategicObjective, Program, Sector
from activitydb.models import ProjectAgreement, ProjectComplete
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from import_export import fields


class IndicatorResource(resources.ModelResource):

    country = fields.Field(column_name='country', attribute='country', widget=ForeignKeyWidget(Country, 'country'))
    indicator_type = fields.Field(column_name='indicator types', attribute='indicator_types')
    objective = fields.Field(column_name='objectives', attribute='objectives_list')
    strategic_objective = fields.Field(column_name='strategic objectives', attribute='strategicobjectives_list')
    program = fields.Field(column_name='program', attribute='programs')
    sector = fields.Field(column_name='sector', attribute='sector', widget=ForeignKeyWidget(Sector, 'sector'))
    level = fields.Field(column_name='levels', attribute='levels')

    class Meta:
        model = Indicator
        exclude = ('create_date','edit_date','owner','id')


class IndicatorAdmin(ImportExportModelAdmin):
    resource_class = IndicatorResource


class CollectedDataResource(resources.ModelResource):

    indicator = fields.Field(column_name='indicator', attribute='indicator',  widget=ForeignKeyWidget(Indicator, 'name_clean'))
    agreement = fields.Field(column_name='agreement', attribute='agreement',  widget=ForeignKeyWidget(ProjectAgreement, 'project_name_clean'))
    complete = fields.Field(column_name='complete', attribute='complete',  widget=ForeignKeyWidget(ProjectComplete, 'project_name_clean'))
    program = fields.Field(column_name='program', attribute='program', widget=ForeignKeyWidget(Program, 'name'))

    class Meta:
        model = CollectedData
        exclude = ('create_date','edit_date')


class CollectedDataAdmin(ImportExportModelAdmin):
    resource_class = CollectedDataResource