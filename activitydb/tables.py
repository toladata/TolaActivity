import django_tables2 as tables
from models import ProjectAgreement

TEMPLATE = '''
<div class="btn-group btn-group-xs">
   <a type="button" class="btn btn-warning" href="/activitydb/projectagreement_update/{{ record.id }}">Edit</a>
   <a type="button" class="btn btn-default" href="/activitydb/projectagreement_detail/{{ record.id }}">View</a>
</div>
'''


class ProjectAgreementTable(tables.Table):
    edit = tables.TemplateColumn(TEMPLATE)

    class Meta:
        model = ProjectAgreement
        attrs = {"class": "paleblue"}
        fields = ('program', 'project_proposal','community', 'activity_code', 'office_code', 'project_name', 'sector', 'project_activity',
                             'project_type', 'account_code', 'sub_code','mc_staff_responsible','total_estimated_budget','mc_estimated_budget')
        sequence = ('program', 'project_proposal','community', 'activity_code', 'office_code', 'project_name', 'sector', 'project_activity',
                             'project_type', 'account_code', 'sub_code','mc_staff_responsible','total_estimated_budget','mc_estimated_budget')

TEMPLATE2 = '''
   <a class="btn btn-default btn-xs" role="button" href="/incident/{{ record.id }}/print">Print</a>
'''