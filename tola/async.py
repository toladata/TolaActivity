import unicodedata
import urllib2
import json
import sys
import requests

from workflow.models import Country, TolaUser, TolaSites, WorkflowLevel1, WorkflowLevel2, Organization
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test


"""
Called from Model on create, update or delete functions passes in the
object label (type) and Name, ID and Related COuntry, Workflowlevels and Org
Create, Update and Delete Workflowlevels and Organizations in TolaScience

create: URL, object, object label
        get token
            authorize
            if object label: level1, level2 or Organization
                post new object

update: URL, object, object label
        get token
            authorize
            if object label: level1, level2 or Organization
                get object by ID

                post update object by ID

delete: URL, object, object label
        get token
            authorize
            if object label: level1, level2 or Organization
                delete object by id

Get new Tables by Org, Country, Workflowlevel and
get: URL, table ID, org, country and workflowlevel
    get token
        authorize
        getAllTables:
            update tolatables object
"""
url = TolaSites.objects.get(site_id=1).url


def get_header():
    token = TolaSites.objects.get(site_id=1).tola_tables_token
    if token:
        headers = {'content-type': 'application/json',
               'Authorization': 'Token ' + token }
    else:
        headers = {'content-type': 'application/json'}
        print "Token Not Found"

    return headers


def get_tables():
    """
    Get table data from a Silo.  First get the Data url from the silo details
    then get data and return it
    :param url: URL to silo meta detail info
    :return: json dump of table data
    """
    response = requests.get(url, headers=get_header(), verify=False)

    print response



