from django.core.management.base import BaseCommand

from indicators.models import Indicator, IndicatorType, CollectedData
from workflow.models import *
from search.models import *
from django.db.models.fields.related import ManyToManyField, RelatedField, ManyToManyRel, ManyToOneRel, ForeignKey

from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError
import os

es = Elasticsearch([os.getenv('ELASTICSEARCH_URL')])

"""
Search index process command

"""


class Command(BaseCommand):
    help = "Start the search index process."

    def add_arguments(self, parser):
        parser.add_argument('index')

    def handle(self, *args, **options):
        print("Starting index process...")
        # TODO add actual index process
        index = options['index']

        update_count = 0
        if index == '_all':
            update_count += self.index_indicators()
            update_count += self.index_collected_data()
            update_count += self.index_workflows()
        elif index == 'workflows':
            update_count += self.index_workflows()
        elif index == 'indicators':
            update_count += self.index_indicators()
        elif index == 'collected_data':
            update_count += self.index_collected_data()

        s = SearchIndexLog()
        s.document_count = update_count
        s.save()

        print("Index process done.")

    def index_workflows(self):
        print("Updating workflowlevel1 model index")

        latest_update = SearchIndexLog.objects.latest("create_date").create_date

        wf1objects = WorkflowLevel1.objects.all().filter(
                create_date__gte=latest_update,
                create_date__lte=datetime.now())
        # index workflowlevel1 objects
        for wf1 in wf1objects:
            # get model field data
            data = self.get_field_data(wf1)

            # aggregate related models
            data['sectors'] = list(map(lambda s: s.sector, wf1.sector.all()))
            data['country'] = list(map(lambda c: self.get_field_data(c), wf1.country.all()))

            # index data with elasticsearch
            try:
                es.index(index="workflows", id=data['level1_uuid'], doc_type='workflow', body=data)
            except RequestError:
                print(wf1, "Error")

        print("Updating workflowlevel2 model index")

        wf2objects = WorkflowLevel2.objects.all().filter(
                create_date__gte=latest_update,
                create_date__lte=datetime.now())
        # index workflowlevel2 objects
        for wf2 in wf2objects:
            # get model field data
            data = self.get_field_data(wf2)

            # aggregate related models
            data['sector'] = wf2.sector.sector if wf2.sector is not None else None
            data['project_type'] = wf2.project_type.name if wf2.project_type is not None else None

            data['workflowlevel1'] = self.get_field_data(wf2.workflowlevel1)
            data['indicators'] = list(map(lambda i: self.get_field_data(i), wf2.indicators.all()))
            data['stakeholder'] = list(map(lambda s: self.get_field_data(s), wf2.stakeholder.all()))
            data['site'] = list(map(lambda s: self.get_field_data(s), wf2.site.all()))

            # index data with elasticsearch
            try:
                es.index(index="workflows", id=data['level2_uuid'], doc_type='workflow', body=data)
            except RequestError:
                print(wf2, "Error")

        return len(wf1objects) + len(wf2objects)

    def index_collected_data(self):
        print("Updating collected data index")

        latest_update = SearchIndexLog.objects.latest("create_date").create_date
        collected_data = CollectedData.objects.all().filter(
                create_date__gte=latest_update,
                create_date__lte=datetime.now())

        for d in collected_data:
            # get model field data
            data = self.get_field_data(d)

            # aggregate related models
            di = d.indicator
            data['indicator'] = di.name

            # index data with elasticsearch
            try:
                es.index(index="collected_data", id=data['data_uuid'], doc_type='data_collection', body=data)
            except RequestError:
                print(d, "Error")
        return len(collected_data)

    def index_indicators(self):
        print("Updating indicator index")

        latest_update = SearchIndexLog.objects.latest("create_date").create_date

        indicators = Indicator.objects.all().filter(
                create_date__gte=latest_update,
                create_date__lte=datetime.now())\
            .prefetch_related('workflowlevel1')


        for i in indicators:
            # get model field data
            data = self.get_field_data(i)

            # aggregate related models
            data['workflowlevel1'] = list(map(lambda w: w.name, i.workflowlevel1.all()))

            # index data with elasticsearch
            try:
                es.index(index="indicators", id=data['id'], doc_type='indicator', body=data)
            except RequestError:
                print(i, "Error")

        return len(indicators)

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
