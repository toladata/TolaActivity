from django.test import TestCase

from indicators.models import Indicator
from search.utils import ElasticsearchIndexer


class ElasticsearchIndexerTest(TestCase):
    def test_es_connection(self):
        indexer = ElasticsearchIndexer()
        self.assertTrue(indexer.es.ping(), "Cannot connect to Elasticsearch")
