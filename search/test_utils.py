import logging
from unittest import skipIf

from django.conf import settings
from django.test import TestCase

import factories
from indicators.models import Indicator
from search.exceptions import ValueNotFoundError
from search.utils import ElasticsearchIndexer
from workflow.models import Organization, WorkflowLevel1, WorkflowLevel2


@skipIf(not settings.ELASTICSEARCH_URL, "Elasticsearch config not found")
class ElasticsearchIndexerTest(TestCase):
    indexer = None

    def setUp(self):
        logging.disable(logging.ERROR)
        settings.ELASTICSEARCH_ENABLED = True
        self.indexer = ElasticsearchIndexer()

    def tearDown(self):
        logging.disable(logging.NOTSET)
        settings.ELASTICSEARCH_ENABLED = False

    def test_es_connection(self):
        self.assertTrue(self.indexer.es.ping(),
                        "Cannot connect to Elasticsearch. URL: {}".format(settings.ELASTICSEARCH_URL))

    def test_create_and_delete_indicator(self):
        indicator = Indicator.objects.create(name="TestIndicator")
        self.indexer.delete_indicator(indicator)

    def test_delete_unexisting_indicator_raises_exception(self):
        org = Organization.objects.create(organization_uuid="not-existing-uuid")
        wflvl1 = factories.WorkflowLevel1(organization=org)
        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        self.indexer.delete_indicator(indicator)

        self.assertRaises(ValueNotFoundError, self.indexer.delete_indicator, indicator)

    def test_create_and_delete_workflowlevel1(self):
        org = Organization.objects.create(organization_uuid="index-workflowlevel1-test")
        wflvl1 = factories.WorkflowLevel1(organization=org)
        self.indexer.delete_workflowlevel1(wflvl1)

    def test_create_and_delete_workflowlevel2(self):
        org = Organization.objects.create(organization_uuid="index-workflowlevel2-test")
        wflvl1 = factories.WorkflowLevel1(organization=org)
        wflvl2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)
        self.indexer.delete_workflowlevel2(wflvl2)

    def test_create_and_delete_collecteddata(self):
        org = Organization.objects.create(organization_uuid="index-collecteddata-test")
        wflvl1 = factories.WorkflowLevel1(organization=org)
        collecteddata = factories.CollectedData(workflowlevel1=wflvl1)
        self.indexer.delete_collecteddata(collecteddata)
