from django.test import TestCase

from indicators.models import Indicator
from search.exceptions import ValueNotFoundError
from search.utils import ElasticsearchIndexer


class ElasticsearchIndexerTest(TestCase):
    def test_es_connection(self):
        indexer = ElasticsearchIndexer()
        self.assertTrue(indexer.es.ping(), "Cannot connect to Elasticsearch")

    def test_create_and_delete_indicator(self):
        indexer = ElasticsearchIndexer()
        indicator = Indicator.objects.create(name="TestIndicator")
        indexer.delete_indicator(indicator.pk)

    def test_delete_unexisting_indicator_raises_exception(self):
        indexer = ElasticsearchIndexer()
        self.assertRaises(ValueNotFoundError, indexer.delete_indicator, 288)
