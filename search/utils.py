import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models.fields.related import ManyToManyField, RelatedField, ManyToManyRel, ManyToOneRel, ForeignKey
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError, NotFoundError

from search.exceptions import ValueNotFoundError

logging.basicConfig()
logger = logging.getLogger(__name__)


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
        prefix = settings.ELASTICSEARCH_INDEX_PREFIX + '_'
    else:
        prefix = ''

    def index_indicator(self, indicator):
        if self.es is None:
            return

        data = self.get_field_data(indicator)

        for wf1 in indicator.workflowlevel1.all():
            if wf1.organization is not None and wf1.organization is not None:
                org_uuid = str(wf1.organization.organization_uuid)

                # aggregate related models
                data['workflowlevel1'] = list(map(lambda w: w.name, [wf1]))

                # index data with elasticsearch
                try:
                    self.es.index(index=self.prefix + org_uuid + "_indicators", id=data['id'], doc_type='indicator',
                             body=data)
                except RequestError:
                    logger.error('Error indexing indicator', exc_info=True)
            else:
                continue

    def delete_indicator(self, indicator):
        if self.es is None:
            return
        try:
            for wf1 in indicator.workflowlevel1.all():
                if wf1.organization is not None:
                    org_uuid = str(wf1.organization.organization_uuid)
                    self.es.delete(index=self.prefix + org_uuid + "_indicators", id=indicator.id, doc_type='indicator')
        except NotFoundError:
            logger.warning('Indicator not found in Elasticsearch', exc_info=True)
            raise ValueNotFoundError

    def index_workflowlevel1(self, wf):
        if self.es is None:
            return

        if wf.organization is not None:
            org_uuid = str(wf.organization.organization_uuid)

            # aggregate related models
            data = self.get_field_data(wf)

            # aggregate related models
            data['sectors'] = list(map(lambda s: s.sector, wf.sector.all()))
            data['country'] = list(map(lambda c: self.get_field_data(c), wf.country.all()))

            # index data with elasticsearch
            try:
                self.es.index(index=self.prefix + org_uuid + "_workflow_level1", id=data['level1_uuid'], doc_type='workflow', body=data)
            except RequestError:
                logger.error('Error indexing workflowlevel1', exc_info=True)

    def index_workflowlevel2(self, wf):
        if self.es is None:
            return

        if wf.workflowlevel1.organization is not None and wf.workflowlevel1.organization is not None:
            org_uuid = str(wf.workflowlevel1.organization.organization_uuid)

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
                self.es.index(index=self.prefix + org_uuid + "_workflow_level2", id=data['level2_uuid'], doc_type='workflow', body=data)
            except RequestError:
                logger.error('Error indexing workflowlevel2', exc_info=True)

    def delete_workflowlevel1(self, wf):
        if self.es is None:
            return

        try:
            if wf.organization is not None and wf.organization is not None:
                org_uuid = str(wf.organization.organization_uuid)

                self.es.delete(index=self.prefix + org_uuid + "_workflow_level1", id=wf.level1_uuid, doc_type='workflow')
        except RequestError:
            logger.error('Error deleting workflowlevel1 from index', exc_info=True)

    def delete_workflowlevel2(self, wf):
        if self.es is None:
            return

        try:
            if wf.workflowlevel1.organization is not None and wf.workflowlevel1.organization is not None:
                org_uuid = str(wf.workflowlevel1.organization.organization_uuid)

                self.es.delete(index=self.prefix + org_uuid + "_workflow_level2", id=wf.level2_uuid, doc_type='workflow')
        except RequestError:
            logger.error('Error deleting workflowlevel2 from index', exc_info=True)

    def index_collecteddata(self, d):
        if self.es is None:
            return

        if d.workflowlevel1 is not None and d.workflowlevel1.organization is not None:
            org_uuid = str(d.workflowlevel1.organization.organization_uuid)

            # get model field data
            data = self.get_field_data(d)

            # aggregate related models
            di = d.indicator
            data['indicator'] = di.name

            # index data with elasticsearch
            try:
                self.es.index(index=self.prefix + org_uuid + "_collected_data", id=data['data_uuid'], doc_type='data_collection', body=data)
            except RequestError:
                logger.error('Error indexing collected data', exc_info=True)

    def delete_collecteddata(self, d):
        if self.es is None:
            return

        try:
            if d.workflowlevel1.organization is not None and d.workflowlevel1.organization is not None:
                org_uuid = str(d.workflowlevel1.organization.organization_uuid)

                self.es.delete(index=self.prefix + org_uuid + "_collected_data", id=d.data_uuid, doc_type='data_collection')
        except RequestError:
            logger.error('Error deleting collected data from index', exc_info=True)

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
