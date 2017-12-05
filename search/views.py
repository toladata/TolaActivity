# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.core.management import call_command
from rest_framework.decorators import api_view

from django.http import HttpResponse

from elasticsearch import Elasticsearch
import json
from django.conf import settings
from workflow.models import TolaUser, ROLE_ORGANIZATION_ADMIN
from indicators.models import Indicator, CollectedData
from tola.util import get_programs_user


if settings.ELASTICSEARCH_URL is not None:
    es = Elasticsearch([settings.ELASTICSEARCH_URL])
else:
    es = None

"""
@login_required(login_url='/accounts/login/')
def search_index(request):
    # TODO remove
    call_command('search-index', '_all')
    return HttpResponse("Index process done.")
"""

@api_view(['GET'])
def search(request, index, term):
    if request.method == 'GET' and es is not None:
        if settings.ELASTICSEARCH_INDEX_PREFIX is not None:
            prefix = settings.ELASTICSEARCH_INDEX_PREFIX + '_'
        else:
            prefix = ''

        user_org_uuid = TolaUser.objects.get(user=request.user).organization.organization_uuid
        prefix = prefix + str(user_org_uuid) + '_'

        index = index.lower().strip('_')  # replace leading _ that _all cannot be accessed directly

        allowed_indices = ['workflow_level1', 'workflow_level2', 'indicators', 'collected_data']
        if index.lower() == 'all':
            index = prefix + 'workflow_level1,' + prefix + 'workflow_level2,' + prefix + 'indicators,' + prefix + 'collected_data'
        elif not index in allowed_indices:
            raise Exception("Index not allowed to access")
        else:
            index = prefix + index

        b = {
            "query": {
                "bool": {
                    "should": [
                        {"match": {
                            "name": {
                                "query": term,
                                "boost": 4
                            }}},
                        {"match": {
                            "sector": {
                                "query": term,
                                "boost": 2
                            }}},
                        {"match": {"workflowlevel1.name": term}},
                        {"match": {"stakeholder.name": term}},
                        {"match": {"site.name": term}}
                    ]
                }
            }
        }
        response = es.search(index=index, body=b)
        results = {"workflowlevel1": [], "workflowlevel2": [], "indicators": [], "collected_data": []}

        # group result by type
        for hit in response["hits"]["hits"]:
            if "workflow_level1" in hit["_index"]:
                results["workflowlevel1"].append(hit)
            elif "workflow_level2" in hit["_index"]:
                results["workflowlevel2"].append(hit)
            elif "indicators" in hit["_index"]:
                results["indicators"].append(hit)
            elif "collected_data" in hit["_index"]:
                results["collected_data"].append(hit)

        # check access
        if not request.user.is_superuser \
            and ROLE_ORGANIZATION_ADMIN not in request.user.groups.values_list(
                    'name', flat=True):
            allowed_wf1s = get_programs_user(request.user)

            wf1_results = []
            for wf1 in results["workflowlevel1"]:
                if wf1["_source"]["id"] in allowed_wf1s:
                    wf1_results.append(wf1)
            results["workflowlevel1"] = wf1_results

            wf2_results = []
            for wf2 in results["workflowlevel2"]:
                if wf2["_source"]["workflowlevel1"]["id"] in allowed_wf1s:
                    wf2_results.append(wf2)
            results["workflowlevel2"] = wf2_results

            i_results = []
            if len(results["indicators"]) > 0:
                allowed_is = list(map(lambda i: i[0], Indicator.objects.values_list("id")
                                      .filter(workflowlevel1__in=allowed_wf1s)))

                for i in results["indicators"]:
                    if i["_source"]["id"] in allowed_is:
                        i_results.append(i)
            results["indicators"] = i_results

            cd_res = []
            if len(results["collected_data"]) > 0:
                allowed_cds = list(map(lambda i: i[0], CollectedData.objects.values_list("id")
                                       .filter(indicator__workflowlevel1__in=allowed_wf1s)))

                for cd in results["collected_data"]:
                    if cd["_source"]["id"] in allowed_cds:
                        cd_res.append(cd)
            results["collected_data"] = cd_res

        return HttpResponse(json.dumps(results), content_type="application/json")
