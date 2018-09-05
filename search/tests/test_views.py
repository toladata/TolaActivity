import json
import logging
from unittest import skipIf

from django.conf import settings
from django.test import TestCase, tag

from rest_framework.test import APIRequestFactory

import factories
from search import views
from search.utils import ElasticsearchIndexer
from workflow.models import Organization, WorkflowLevel1, ROLE_PROGRAM_ADMIN


@tag('pkg')
@skipIf(not settings.ELASTICSEARCH_URL, "Elasticsearch config not found")
class ElasticsearchSearchTest(TestCase):
    indexer = None

    def setUp(self):
        logging.disable(logging.ERROR)
        settings.ELASTICSEARCH_ENABLED = True
        self.org = Organization.objects.create(
            organization_uuid="index-workflowlevel1-test")
        self.indexer = ElasticsearchIndexer()
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser(organization=self.org)

    def tearDown(self):
        logging.disable(logging.NOTSET)
        settings.ELASTICSEARCH_ENABLED = False

    def test_es_connection(self):
        self.assertTrue(self.indexer.es.ping(),
                        "Cannot connect to Elasticsearch. URL: {}".format(
                            settings.ELASTICSEARCH_URL))

    def test_search_for_workflowlevel1(self):
        wflvl1s = factories.WorkflowLevel1.create_batch(
            15, organization=self.org)
        role_program_admin = factories.Group(name=ROLE_PROGRAM_ADMIN)

        for wflvl1 in wflvl1s:
            factories.WorkflowTeam(
                workflow_user=self.tola_user,
                workflowlevel1=wflvl1,
                role=role_program_admin
            )

        # get data from all the indexes
        request = self.factory.get('')
        request.user = self.tola_user.user
        response = views.search(request, '_all', 'health')
        content = json.loads(response.content)

        # we have data only for workflowlevel1
        self.assertTrue(len(content['workflowlevel1']) > 0)
        self.assertTrue(len(content['workflowlevel2']) == 0)
        self.assertTrue(len(content['indicators']) == 0)
        self.assertTrue(len(content['collected_data']) == 0)

        wflvl1_1 = content['workflowlevel1'][0]['_source']
        search_after = content['workflowlevel1'][0]['sort']

        # get more data using the cursor
        request = self.factory.get('?search_after={},{}'.format(
            search_after[0], search_after[1]))
        request.user = self.tola_user.user
        response = views.search(request, '_workflow_level1', 'health')
        content = json.loads(response.content)

        self.assertTrue(len(content['workflowlevel1']) > 0)

        wflvl1_2 = content['workflowlevel1'][0]['_source']
        self.assertNotEqual(wflvl1_1['level1_uuid'], wflvl1_2['level1_uuid'])

    def test_search_for_workflowlevel2(self):
        role_program_admin = factories.Group(name=ROLE_PROGRAM_ADMIN)
        wflvl1 = factories.WorkflowLevel1(organization=self.org)
        factories.WorkflowTeam(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=role_program_admin
        )
        factories.WorkflowLevel2.create_batch(15, workflowlevel1=wflvl1)

        # get data from all the indexes
        request = self.factory.get('')
        request.user = self.tola_user.user
        response = views.search(request, '_all', 'help')
        content = json.loads(response.content)

        # we have data only for workflowlevel2
        self.assertTrue(len(content['workflowlevel1']) == 0)
        self.assertTrue(len(content['workflowlevel2']) > 0)
        self.assertTrue(len(content['indicators']) == 0)
        self.assertTrue(len(content['collected_data']) == 0)

        wflvl2_1 = content['workflowlevel2'][0]['_source']
        search_after = content['workflowlevel2'][0]['sort']

        # get more data using the cursor
        request = self.factory.get('?search_after={},{}'.format(
            search_after[0], search_after[1]))
        request.user = self.tola_user.user
        response = views.search(request, '_workflow_level2', 'help')

        content = json.loads(response.content)
        self.assertTrue(len(content['workflowlevel2']) > 0)

        wflvl2_2 = content['workflowlevel2'][0]['_source']
        self.assertNotEqual(wflvl2_1['level2_uuid'], wflvl2_2['level2_uuid'])

    def test_search_for_indicator(self):
        role_program_admin = factories.Group(name=ROLE_PROGRAM_ADMIN)
        wflvl1 = factories.WorkflowLevel1(organization=self.org)
        factories.WorkflowTeam(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=role_program_admin
        )
        factories.Indicator.create_batch(15, workflowlevel1=[wflvl1])

        # get data from all the indexes
        request = self.factory.get('')
        request.user = self.tola_user.user
        response = views.search(request, '_all', 'building')
        content = json.loads(response.content)

        # we have data only for indicator
        self.assertTrue(len(content['workflowlevel1']) == 0)
        self.assertTrue(len(content['workflowlevel2']) == 0)
        self.assertTrue(len(content['indicators']) > 0)
        self.assertTrue(len(content['collected_data']) == 0)

        indicator_1 = content['indicators'][0]['_source']
        search_after = content['indicators'][0]['sort']

        # get more data using the cursor
        request = self.factory.get('?search_after={},{}'.format(
            search_after[0], search_after[1]))
        request.user = self.tola_user.user
        response = views.search(request, '_indicators', 'building')

        content = json.loads(response.content)
        self.assertTrue(len(content['indicators']) > 0)

        indicator_2 = content['indicators'][0]['_source']
        self.assertNotEqual(indicator_1['indicator_uuid'],
                            indicator_2['indicator_uuid'])
