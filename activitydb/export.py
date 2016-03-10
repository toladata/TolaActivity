from import_export import resources
from import_export.widgets import ForeignKeyWidget, ManyToManyWidget
from import_export import fields
from .models import TrainingAttendance, Beneficiary, ProjectAgreement, Program, SiteProfile, Capacity, Evaluate, Stakeholder


class TrainingAttendanceResource(resources.ModelResource):

    class Meta:
        model = TrainingAttendance


class BeneficiaryResource(resources.ModelResource):

    class Meta:
        model = Beneficiary


class ProjectAgreementResource(resources.ModelResource):
    sites = fields.Field(column_name='sites', attribute='sites', widget=ManyToManyWidget(SiteProfile, 'name'))
    capacity = fields.Field(column_name='capacity', attribute='capacity', widget=ManyToManyWidget(Capacity, 'capacity'))
    evaluate = fields.Field(column_name='evaluate', attribute='evaluate', widget=ManyToManyWidget(Evaluate, 'evaluate'))
    stakeholder = fields.Field(column_name='stakeholder', attribute='stakeholder', widget=ManyToManyWidget(Stakeholder, 'name'))

    class Meta:
        model = ProjectAgreement


class ProgramResource(resources.ModelResource):

    class Meta:
        model = Program
