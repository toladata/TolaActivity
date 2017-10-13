#add global variable for report server or not to all templates so we can hide elements that aren't wanted on the report server
from settings.local import REPORT_SERVER
from settings.local import OFFLINE_MODE
from settings.local import NON_LDAP
from workflow.models import Organization

from django.conf import settings

def report_server_check(request):
    return {'report_server': REPORT_SERVER, 'offline_mode': OFFLINE_MODE, 'non_ldap': NON_LDAP}



# get the organization labels from the user for each level of workflow for display in templates
def org_levels(request):

    try:
        getOrg = Organization.objects.get(id=request.user.tola_user.country.organization.id)
        workflowlevel1 = getOrg.level_1_label
        workflowlevel2 = getOrg.level_2_label
        workflowlevel3 = getOrg.level_3_label
    except Exception, e:
        workflowlevel1 = "Program"
        workflowlevel2 = "Projects"
        workflowlevel3 = "Activity"

    return {'WORKFLOWLEVEL1': workflowlevel1, 'WORKFLOWLEVEL2': workflowlevel2, 'WORKFLOWLEVEL3': workflowlevel3}

def google_analytics(request):
    """
    Use the variables returned in this function to render Google Analytics Tracking Code template.
    """

    ga_prop_id = getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_ID', False)
    ga_domain = getattr(settings, 'GOOGLE_ANALYTICS_DOMAIN', False)

    if not settings.DEBUG and ga_prop_id and ga_domain:
        return {
            'GOOGLE_ANALYTICS_PROPERTY_ID': ga_prop_id,
            'GOOGLE_ANALYTICS_DOMAIN': ga_domain,
        }
    return {}

