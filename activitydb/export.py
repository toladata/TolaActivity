from import_export import resources
from .models import TrainingAttendance, Beneficiary, ProjectAgreement


class TrainingAttendanceResource(resources.ModelResource):

    class Meta:
        model = TrainingAttendance


class BeneficiaryResource(resources.ModelResource):

    class Meta:
        model = Beneficiary


class ProjectAgreementResource(resources.ModelResource):

    class Meta:
        model = ProjectAgreement