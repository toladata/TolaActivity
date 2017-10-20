from django.conf import settings
from django.core.management.base import BaseCommand

from search.models import *
from django.db.models.fields.related import ManyToManyField, RelatedField, ManyToManyRel, ManyToOneRel, ForeignKey

from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
import os


class ElasticsearchIndexer:
    """
    Adds an index process for each indicators, workflowlevel 1 and 2 and collecteddata models
    To seperate indices of different servers a prefix can be defined in settings
    """
    if settings.ELASTICSEARCH_URL is not None:
        es = Elasticsearch([settings.ELASTICSEARCH_URL], timeout=30, max_retries=10, retry_on_timeout=True)
    else:
        es = None

    if settings.ELASTICSEARCH_INDEX_PREFIX is not None:
        prefix = settings.ELASTICSEARCH_INDEX_PREFIX+'_'
    else:
        prefix = ''

    def index_indicator(self, i):
        if self.es is None:
            return

        data = self.get_field_data(i)

        # aggregate related models
        data['workflowlevel1'] = list(map(lambda w: w.name, i.workflowlevel1.all()))

        # index data with elasticsearch
        try:
            self.es.index(index=self.prefix+"indicators", id=data['id'], doc_type='indicator', body=data)
        except RequestError:
            print(i, "Error")   # Todo write to error log

    def delete_indicator(self, id):
        if self.es is None:
            return

        try:
            self.es.delete(index=self.prefix+"indicators", id=id, doc_type='indicator')
        except RequestError:
            print(id, "Error")   # Todo write to error log

    def index_workflowlevel1(self, wf):
        if self.es is None:
            return
        data = self.get_field_data(wf)

        # aggregate related models
        data = self.get_field_data(wf)

        # aggregate related models
        data['sectors'] = list(map(lambda s: s.sector, wf.sector.all()))
        data['country'] = list(map(lambda c: self.get_field_data(c), wf.country.all()))

        # index data with elasticsearch
        try:
            self.es.index(index=self.prefix+"workflows", id=data['level1_uuid'], doc_type='workflow', body=data)
        except RequestError:
            print(wf, "Error")  # Todo write to error log

    def index_workflowlevel2(self, wf):
        if self.es is None:
            return

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
            self.es.index(index=self.prefix+"workflows", id=data['level2_uuid'], doc_type='workflow', body=data)
        except RequestError:
            print(wf, "Error")

    def delete_workflows(self, id):
        if self.es is None:
            return

        try:
            self.es.delete(index=self.prefix+"workflows", id=id, doc_type='workflow')
        except RequestError:
            print(id, "Error")   # Todo write to error log

    def index_collecteddata(self, d):
        if self.es is None:
            return

        # get model field data
        data = self.get_field_data(d)

        # aggregate related models
        di = d.indicator
        data['indicator'] = di.name

        # index data with elasticsearch
        try:
            self.es.index(index=self.prefix+"collected_data", id=data['data_uuid'], doc_type='data_collection', body=data)
        except RequestError:
            print(d, "Error")   # Todo write to error log

    def delete_collecteddata(self, id):
        if self.es is None:
            return

        try:
            self.es.delete(index=self.prefix+"collected_data", id=id, doc_type='data_collection')
        except RequestError:
            print(id, "Error")   # Todo write to error log

    def get_field_data(self, obj):
        if self.es is None:
            return

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
