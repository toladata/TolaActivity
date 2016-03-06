from import_export import resources
from .models import TrainingAttendance, Beneficiary, ProjectAgreement, Program


class TrainingAttendanceResource(resources.ModelResource):

    class Meta:
        model = TrainingAttendance


class BeneficiaryResource(resources.ModelResource):

    class Meta:
        model = Beneficiary


class ProjectAgreementResource(resources.ModelResource):

    class Meta:
        model = ProjectAgreement


class ProgramResource(resources.ModelResource):

    class Meta:
        model = Program
