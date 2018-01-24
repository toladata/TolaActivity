import requests
import logging
import json
from urlparse import urljoin

from django.conf import settings

logger = logging.getLogger(__name__)


def register_user(data, tolauser):
    headers = {
        'Authorization': 'Token {}'.format(settings.TOLA_TRACK_TOKEN),
    }

    url_subpath = 'accounts/register/'
    url = urljoin(settings.TOLA_TRACK_URL, url_subpath)

    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 201:
        logger.info("The TolaUser {} (id={}) was created successfully on "
                    "Track.".format(tolauser.name, tolauser.id))
    elif response.status_code in [400, 403]:
        logger.warning("The TolaUser {} (id={}) could not be created "
                       "successfully on Track.".format(
                        tolauser.name, tolauser.id))
    return response


def create_workflowlevel1(obj):
    headers = {
        'Authorization': 'Token {}'.format(settings.TOLA_TRACK_TOKEN),
    }

    url_subpath = 'api/organization?name={}'.format(obj.organization.name)
    url = urljoin(settings.TOLA_TRACK_URL, url_subpath)
    response = requests.get(url, headers=headers)
    if response.status_code in [400, 403, 500]:
        logger.warn('The Organization {} (id={}) could not be '
                    'successfully fetched from Track.'.format(
                     obj.organization.name, obj.organization.id))
        return response

    content = json.loads(response.content)
    if response.status_code == 200 and len(content) == 0:
        logger.info('The organization {} (id={}) was not found on Track'.format(
            obj.organization.name, obj.organization.id))
        return response

    org = content[0]
    data = {
        'level1_uuid': obj.level1_uuid,
        'name': obj.name,
        'country': None,
        'organization': org['id']
    }

    url_subpath = 'api/workflowlevel1'
    url = urljoin(settings.TOLA_TRACK_URL, url_subpath)
    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 201:
        logger.info('The Program {} (id={}) was created successfully on '
                    'Track.'.format(obj.name, obj.id))
    return response
