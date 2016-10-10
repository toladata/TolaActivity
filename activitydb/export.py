from import_export import resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from import_export import fields
from .models import TrainingAttendance, Distribution, Beneficiary, ProjectAgreement, Program, SiteProfile, Capacity, Evaluate, \
    Stakeholder, Sector, ProjectType, Office, TolaUser, ProjectComplete


class TrainingAttendanceResource(resources.ModelResource):

    class Meta:
        model = TrainingAttendance


class DistributionResource(resources.ModelResource):

    class Meta:
        model = Distribution


class BeneficiaryResource(resources.ModelResource):

    class Meta:
        model = Beneficiary


class ProjectAgreementResource(resources.ModelResource):
    site = fields.Field(column_name='site', attribute='site', widget=ManyToManyWidget(SiteProfile, 'name'))
    capacity = fields.Field(column_name='capacity', attribute='capacity', widget=ManyToManyWidget(Capacity, 'capacity'))
    evaluate = fields.Field(column_name='evaluate', attribute='evaluate', widget=ManyToManyWidget(Evaluate, 'evaluate'))
    stakeholder = fields.Field(column_name='stakeholder', attribute='stakeholder', widget=ManyToManyWidget(Stakeholder, 'name'))
    program = fields.Field(column_name='program', attribute='program', widget=ForeignKeyWidget(Program, 'name'))
    sector = fields.Field(column_name='sector', attribute='sector', widget=ForeignKeyWidget(Sector, 'sector'))
    project_type = fields.Field(column_name='project_type', attribute='project_type', widget=ForeignKeyWidget(ProjectType, 'name'))
    office = fields.Field(column_name='office', attribute='office', widget=ForeignKeyWidget(Office, 'code'))
    estimated_by = fields.Field(column_name='estimated_by', attribute='estimated_by', widget=ForeignKeyWidget(TolaUser, 'name'))
    approved_by = fields.Field(column_name='approved_by', attribute='approved_by', widget=ForeignKeyWidget(TolaUser, 'name'))

    class Meta:
        model = ProjectAgreement


class ProjectCompleteResource(resources.ModelResource):
    site = fields.Field(column_name='site', attribute='site', widget=ManyToManyWidget(SiteProfile, 'name'))
    capacity = fields.Field(column_name='capacity', attribute='capacity', widget=ManyToManyWidget(Capacity, 'capacity'))
    evaluate = fields.Field(column_name='evaluate', attribute='evaluate', widget=ManyToManyWidget(Evaluate, 'evaluate'))
    stakeholder = fields.Field(column_name='stakeholder', attribute='stakeholder', widget=ManyToManyWidget(Stakeholder, 'name'))
    program = fields.Field(column_name='program', attribute='program', widget=ForeignKeyWidget(Program, 'name'))
    sector = fields.Field(column_name='sector', attribute='sector', widget=ForeignKeyWidget(Sector, 'sector'))
    project_type = fields.Field(column_name='project_type', attribute='project_type', widget=ForeignKeyWidget(ProjectType, 'name'))
    office = fields.Field(column_name='office', attribute='office', widget=ForeignKeyWidget(Office, 'code'))
    estimated_by = fields.Field(column_name='estimated_by', attribute='estimated_by', widget=ForeignKeyWidget(TolaUser, 'name'))
    approved_by = fields.Field(column_name='approved_by', attribute='approved_by', widget=ForeignKeyWidget(TolaUser, 'name'))

    class Meta:
        model = ProjectComplete


class ProgramResource(resources.ModelResource):

    class Meta:
        model = Program

class StakeholderResource(resources.ModelResource):
    class Meta:
        model = Stakeholder
            
        
