# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from search.utils import ElasticsearchIndexer
from elasticsearch.exceptions import RequestError, NotFoundError
from search.exceptions import ValueNotFoundError


@shared_task(bind=True, max_retries=3)
def async_index_indicator(self, indicator):
    try:
        ei = ElasticsearchIndexer()
        ei.index_indicator(indicator)
    except RequestError as exc:
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3)
def async_delete_indicator(self, indicator):
    try:
        ei = ElasticsearchIndexer()
        ei.delete_indicator(indicator)
    except RequestError as exc:
        raise self.retry(exc=exc)
    except ValueNotFoundError:
        pass



@shared_task(bind=True, max_retries=3)
def async_index_collecteddata(self, collecteddata):
    try:
        ei = ElasticsearchIndexer()
        ei.index_collecteddata(collecteddata)
    except RequestError as exc:
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3)
def async_delete_collecteddata(self, collecteddata):
    try:
        ei = ElasticsearchIndexer()
        ei.delete_collecteddata(collecteddata)
    except RequestError as exc:
        raise self.retry(exc=exc)
    except ValueNotFoundError:
        pass


@shared_task(bind=True, max_retries=3)
def async_index_workflowlevel1(self, wf1):
    try:
        ei = ElasticsearchIndexer()
        ei.index_workflowlevel1(wf1)
    except RequestError as exc:
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3)
def async_delete_workflowlevel1(self, wf1):
    try:
        ei = ElasticsearchIndexer()
        ei.delete_workflowlevel1(wf1)
    except RequestError as exc:
        raise self.retry(exc=exc)
    except ValueNotFoundError:
        pass


@shared_task(bind=True, max_retries=3)
def async_index_workflowlevel2(self, wf2):
    try:
        ei = ElasticsearchIndexer()
        ei.index_workflowlevel2(wf2)
    except RequestError as exc:
        raise self.retry(exc=exc)


@shared_task(bind=True, max_retries=3)
def async_delete_workflowlevel2(self, wf2):
    try:
        ei = ElasticsearchIndexer()
        ei.delete_workflowlevel2(wf2)
    except RequestError as exc:
        raise self.retry(exc=exc)
    except ValueNotFoundError:
        pass
