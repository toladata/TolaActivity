from unittest import skipIf
import factories

from django.conf import settings
from django.test import TestCase

from indicators.models import Indicator
from workflow.models import Organization, WorkflowLevel1, WorkflowLevel2
from search.exceptions import ValueNotFoundError
from search.utils import ElasticsearchIndexer


@skipIf(not settings.ELASTICSEARCH_URL, "Elasticsearch config not found")
class ElasticsearchIndexerTest(TestCase):
    def test_es_connection(self):
        indexer = ElasticsearchIndexer()
        self.assertTrue(indexer.es.ping(),
                        "Cannot connect to Elasticsearch. URL: {}".format(settings.ELASTICSEARCH_URL))

    def test_create_and_delete_indicator(self):
        indexer = ElasticsearchIndexer()
        indicator = Indicator.objects.create(name="TestIndicator")
        indexer.delete_indicator(indicator)

    def test_delete_unexisting_indicator_raises_exception(self):
        indexer = ElasticsearchIndexer()
        org = Organization.objects.create(organization_uuid="not-existing-uuid")
        wflvl1 = factories.WorkflowLevel1(organization=org)
        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        indexer.delete_indicator(indicator)

        self.assertRaises(ValueNotFoundError, indexer.delete_indicator, indicator)

    def test_create_and_delete_workflowlevel1(self):
        indexer = ElasticsearchIndexer()
        org = Organization.objects.create(organization_uuid="index-workflowlevel1-test")
        wflvl1 = factories.WorkflowLevel1(organization=org)
        indexer.delete_workflowlevel1(wflvl1)

    def test_create_and_delete_workflowlevel2(self):
        indexer = ElasticsearchIndexer()
        org = Organization.objects.create(organization_uuid="index-workflowlevel2-test")
        wflvl1 = factories.WorkflowLevel1(organization=org)
        wflvl2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)
        indexer.delete_workflowlevel2(wflvl2)

    def test_create_and_delete_collecteddata(self):
        indexer = ElasticsearchIndexer()
        org = Organization.objects.create(organization_uuid="index-collecteddata-test")
        wflvl1 = factories.WorkflowLevel1(organization=org)
        collecteddata = factories.CollectedData(workflowlevel1=wflvl1)
        indexer.delete_collecteddata(collecteddata)
