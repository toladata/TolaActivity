from django.conf import settings
from django.core.management.base import BaseCommand

from indicators.models import *
from workflow.models import *
from search.models import *
from django.db.models.fields.related import ManyToManyField, RelatedField, ManyToManyRel, ManyToOneRel, ForeignKey

from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
import os


class ElasticsearchIndexer:
    es = Elasticsearch([settings.ELASTICSEARCH_URL])

    def index_indicator(self, i):
        data = self.get_field_data(i)

        # aggregate related models
        data['workflowlevel1'] = list(map(lambda w: w.name, i.workflowlevel1.all()))

        # index data with elasticsearch
        try:
            self.es.index(index="indicators", id=data['id'], doc_type='indicator', body=data)
        except RequestError:
            print(i, "Error")

    def update_indicator(self, i):
        data = self.get_field_data(i)

        # aggregate related models
        data['workflowlevel1'] = list(map(lambda w: w.name, i.workflowlevel1.all()))

        # index data with elasticsearch
        try:
            self.es.update(index="indicators", id=data['id'], doc_type='indicator', body=data)
        except RequestError:
            print(i, "Error")

    def delete_indicator(self, i):
        data = self.get_field_data(i)

        try:
            self.es.delete(index="indicators", id=data['id'], doc_type='indicator')
        except RequestError:
            print(i, "Error")

    def get_field_data(self, obj):
        """
        Returns all field data that is stored in a related model
        :param obj: the object to retrieve data from
        :return: dict of object data with field names as keys
        """
        data = {}
        for f in obj._meta.get_fields():
            if type(f) is not ManyToManyField \
                    and type(f) is not ManyToManyRel \
                    and type(f) is not ManyToOneRel \
                    and type(f) is not ForeignKey \
                    and type(f) is not RelatedField:
                data[f.name] = getattr(obj, f.name)
        return data
