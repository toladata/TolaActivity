from unittest import skipIf

from django.conf import settings
from django.test import TestCase

from indicators.models import Indicator
from workflow.models import Organization, WorkflowLevel1
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

    """
    Disabled because an indicator object needs to exist in database to add a workflowlevel1 many to many relation
    def test_delete_unexisting_indicator_raises_exception(self):
        indexer = ElasticsearchIndexer()
        org = Organization.objects.create(organization_uuid="not-existing-uuid")
        wf1 = WorkflowLevel1.objects.create(organization=org)
        indicator = Indicator(name="NotExistingIndicator", id=999, workflowlevel1=[wf1])
        self.assertRaises(ValueNotFoundError, indexer.delete_indicator, indicator)
    """