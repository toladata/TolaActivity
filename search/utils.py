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
    if settings.ELASTICSEARCH_URL is not None:
        es = Elasticsearch([settings.ELASTICSEARCH_URL])
    else:
        es = None

    def index_indicator(self, i):
        data = self.get_field_data(i)

        # aggregate related models
        data['workflowlevel1'] = list(map(lambda w: w.name, i.workflowlevel1.all()))

        # index data with elasticsearch
        try:
            self.es.index(index="indicators", id=data['id'], doc_type='indicator', body=data)
        except RequestError:
            print(i, "Error")   # Todo write to error log

    def delete_indicator(self, id):
        try:
            self.es.delete(index="indicators", id=id, doc_type='indicator')
        except RequestError:
            print(id, "Error")   # Todo write to error log

    def index_workflowlevel1(self, wf):
        data = self.get_field_data(wf)

        # aggregate related models
        data = self.get_field_data(wf)

        # aggregate related models
        data['sectors'] = list(map(lambda s: s.sector, wf.sector.all()))
        data['country'] = list(map(lambda c: self.get_field_data(c), wf.country.all()))

        # index data with elasticsearch
        try:
            self.es.index(index="workflows", id=data['level1_uuid'], doc_type='workflow', body=data)
        except RequestError:
            print(wf, "Error")  # Todo write to error log

    def index_workflowlevel2(self, wf):
        # get model field data
        data = self.get_field_data(wf)

        # aggregate related models
        data['sector'] = wf.sector.sector if wf.sector is not None else None

        data['workflowlevel1'] = self.get_field_data(wf.workflowlevel1)
        data['indicators'] = list(map(lambda i: self.get_field_data(i), wf.indicators.all()))
        data['stakeholder'] = list(map(lambda s: self.get_field_data(s), wf.stakeholder.all()))
        data['site'] = list(map(lambda s: self.get_field_data(s), wf.site.all()))

        # index data with elasticsearch
        try:
            self.es.index(index="workflows", id=data['level2_uuid'], doc_type='workflow', body=data)
        except RequestError:
            print(wf, "Error")

    def delete_workflows(self, id):
        try:
            self.es.delete(index="workflows", id=id, doc_type='workflow')
        except RequestError:
            print(id, "Error")   # Todo write to error log

    def index_collecteddata(self, d):
        # get model field data
        data = self.get_field_data(d)

        # aggregate related models
        di = d.indicator
        data['indicator'] = di.name

        # index data with elasticsearch
        try:
            self.es.index(index="collected_data", id=data['data_uuid'], doc_type='data_collection', body=data)
        except RequestError:
            print(d, "Error")   # Todo write to error log

    def delete_collecteddata(self, id):
        try:
            self.es.delete(index="collected_data", id=id, doc_type='data_collection')
        except RequestError:
            print(id, "Error")   # Todo write to error log

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
