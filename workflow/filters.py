import django_filters
from models import WorkflowLevel2

class ProjectAgreementFilter(django_filters.FilterSet):

    class Meta:
        model = WorkflowLevel2
        fields = ['activity_code', 'project_name', 'beneficiary_type','workflowlevel1','sector']

    def __init__(self, *args, **kwargs):
        super(ProjectAgreementFilter, self).__init__(*args, **kwargs)
