import requests
from workflow.models import Country, TolaUser, TolaSites, Organization, WorkflowLevel1, WorkflowLevel2


def get_headers():
    """
    Authentication for Tables
    Get the header information to send to tables in the request
    :return: headers
    """
    tables = TolaSites.objects.get(site_id=1)
    if tables.tola_tables_token:
        headers = {'content-type': 'application/json',
                   'Authorization': 'Token ' + tables.tola_tables_token}
    else:
        headers = {'content-type': 'application/json'}
        print "Token Not Found"

    return headers


def send_to_tables(section,payload,id):
    """
    send the requests to individual API endpoint in tables
    with the payload and id
    :param section: model class on tables and activity
    :return: status: success of failure of request
    """
    status = "unknown"
    headers = get_headers()

    # get the table URL
    tables = TolaSites.objects.get(site_id=1)

    post_url = tables.tola_tables_url + "api/" + section + "/" + id
    resp = requests.post(post_url, json=payload, headers=headers, verify=False)

    if resp.status_code == "405":
        post_url = tables.tola_tables_url + "api/" + section + "/"
        resp = requests.post(post_url, json=payload, headers=headers, verify=False)

    if resp.status_code == "200":
        status = "success"

    return status


def check_org(org):
    """
    Get or create the org in Tables
    :param org:
    :return: the org URL in tables
    """
    org_url = None
    headers = get_headers()
    payload = {'name': org}

    # get the table URL
    tables = TolaSites.objects.get(site_id=1)
    check_org_url = tables.tola_tables_url + "api/organization/?name=" + org
    check_resp = requests.get(check_org_url, json=payload, headers=headers, verify=False)

    if check_resp == "405":
        post_org_url = tables.tola_tables_url + "api/organization/"
        payload = {"name": org}
        post_resp = requests.post(post_org_url, json=payload, headers=headers, verify=False)

    if post_resp == "200":
        org_url = check_org_url

    return org_url


def update_level1():
    """
    Update or create each workflowlevel1 in tables
    :return:
    """
    # update TolaTables with program data
    Level1 = WorkflowLevel1.objects.all()

    # check the org exists
    organization = Organization.objects.all()
    for org in organization:
        org_url = check_org(org)

    get_level_1_org = Organization.objects.get(country=Level1.country)
    print Level1.countries

    # each level1 send to tables
    for item in Level1:
        payload = {'level1_uuid': item.level1_uuid, 'name': item.name, 'organization': org_url}
        send_to_tables(section="workflowlevel1", json=payload)


def update_level2():
    """
    Update or create each workflowlevel1 in tables
    :return:
    """
    # update TolaTables with program data
    Level2 = WorkflowLevel2.objects.all()

    # check the org exists
    organization = Organization.objects.get(country=Level2[0].country).name
    org_url = check_org(organization)

    # each level1 send to tables
    for item in Level2:
        payload = {'level2_uuid': item.level2_uuid, 'name': item.name, 'organization': org_url}
        send_to_tables(section="workflowlevel2", json=payload)

