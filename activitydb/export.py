from import_export import resources
from .models import TrainingAttendance, Beneficiary


class TrainingAttendanceResource(resources.ModelResource):

    class Meta:
        model = TrainingAttendance


class BeneficiaryResource(resources.ModelResource):

    class Meta:
        model = Beneficiary