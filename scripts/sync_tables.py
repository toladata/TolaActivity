"""
import json data from API
IMPORTANT!! you must turn off pagination for this to work from a URL and get all
country records
Install module django-extensions
Runs twice via function calls at bottom once
"""
import json
import requests

from workflow.models import Country, TolaUser, TolaSites, Organization, WorkflowLevel1, WorkflowLevel2


def _get_headers():
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


def _send_to_tables(section,payload, id):
    """
    send the requests to individual API endpoint in tables
    with the payload and id
    :param section: model class on tables and activity
    :return: status: success of failure of request
    """
    headers = _get_headers()

    # get the table URL
    tables = TolaSites.objects.get(site_id=1)

    print "COMMENT POST TO TABLES"
    post_url = tables.tola_tables_url + "api/" + section + "/" + str(id)
    print post_url
    resp = requests.post(post_url, json=payload, headers=headers, verify=False)
    status = resp.reason + " : " + str(resp.status_code)
    print status

    if str(resp.status_code) == "405":
        print "COMMENT 405 means it likely does not exist so create a new one"
        post_url = tables.tola_tables_url + "api/" + section
        print post_url
        resp = requests.post(post_url, json=payload, headers=headers, verify=False)
        status = resp.reason
        print resp.content

    if str(resp.status_code) == "200":
        status = "success"

    return status


def _check_org(org):
    """
    Get or create the org in Tables
    :param org:
    :return: the org URL in tables
    """
    status = None
    headers = _get_headers()

    # get the table URL
    tables = TolaSites.objects.get(site_id=1)
    check_org_url = tables.tola_tables_url + "api/organization?format=json&name=" + org
    check_resp = requests.get(check_org_url, headers=headers, verify=False)

    print check_resp.content
    data = json.loads(check_resp.content)

    if not data:
        # print "COMMENT REPOST TO CREATE ORG"
        post_org_url = tables.tola_tables_url + "api/organization"
        payload = {"name": org}
        post_resp = requests.post(post_org_url, json=payload, headers=headers, verify=False)
        org_url = post_org_url

        status = "post_resp=" + str(post_resp.status_code) + " " + post_org_url

        print status
        # print "COMMENT RECHECK ORG"
        check_org_url = tables.tola_tables_url + "api/organization?format=json&name=" + org
        check_resp = requests.get(check_org_url, headers=headers, verify=False)

        status = "check_org=" + str(check_resp.status_code) + " " + org_url
        # get data response from post
        data = json.loads(check_resp.content)

    print data[0]
    org_id = str(data[0]['id'])

    print status

    return org_id


def update_level1():
    """
    Update or create each workflowlevel1 in tables
    :return:
    """
    # update TolaTables with program data
    Level1 = WorkflowLevel1.objects.all()

    # each level1 send to tables
    for item in Level1:
        print item.countries
        # check to see if the organization exists on tables first if not it check_org will create it
        get_org = Organization.objects.all().get(country__country=item.countries)
        org_id = _check_org(get_org.name)
        # set payload and deliver
        print org_id
        payload = {'level1_uuid': item.level1_uuid, 'name': item.name, 'organization': org_id}
        print payload
        send = _send_to_tables(section="workflowlevel1", payload=payload, id=item.id)

        print send


def update_level2():
    """
    Update or create each workflowlevel1 in tables
    :return:
    """
    # update TolaTables with program data
    Level2 = WorkflowLevel2.objects.all()

    # each level1 send to tables
    for item in Level2:
        print item.workflowlevel1.countries
        # check to see if the organization exists on tables first if not it check_org will create it
        get_org = Organization.objects.all().get(country__country=item.workflowlevel1.countries)
        org_id = _check_org(get_org.name)

        level1_id = _check_org(item.workflowlevel1.level1_uuid)
        # set payload and deliver to tables
        payload = {'level2_uuid': item.level2_uuid, 'name': item.name, 'organization': org_id, 'workflowlevel1': level1_id}
        send = _send_to_tables(section="workflowlevel2", payload=payload, id=item.id)

        print send


def run():
    print "Running Script..."
    try:
        update_level1()
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))

    try:
        update_level2()
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))

