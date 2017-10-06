# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.management import call_command
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view

from rest_framework.pagination import PageNumberPagination
from .models import SearchIndexLog
from django.http import HttpResponse

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
import os
import json
from django.conf import settings


if settings.ELASTICSEARCH_URL is not None:
    es = Elasticsearch([settings.ELASTICSEARCH_URL])
else:
    es = None


@login_required(login_url='/accounts/login/')
def search_index(request):
    call_command('search-index', '_all')
    return HttpResponse("Index process done.")


@api_view(['GET'])
def search(request, index, term):
    if request.method == 'GET' and es is not None:
        index = index.lower().replace('_', '')      # replace _ that _all cannot be accessed directly

        allowed_indices = ['workflows','indicators','collected_data']
        if index.lower() == 'all':
            index = 'workflows,indicators,collected_data'
        elif not index in allowed_indices:
            raise Exception("Index not allowed to access")

        # TODO verify access permissions
        """
        To verify user permissions the following options are possible.
        1 - use xpack security and add the organisation user to the config. 
            Anything accessed by this user will be checked by xpack
        
        2 - add a user/organisation or group field to search index. 
            On search action filter for this field
            
        """
        b = {
          "query": {
            "bool": {
              "should": [
                {"match": {
                    "name":  {
                      "query": term,
                      "boost": 4
                }}},
                {"match": {
                    "sector":  {
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
        results = es.search(index=index, body=b)

        return HttpResponse(json.dumps(results["hits"]), content_type="application/json")
