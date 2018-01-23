import requests
import logging
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
        logger.info("The TolaUser {} (id={}) was created successfully in "
                    "Track.".format(tolauser.name, tolauser.id))
    elif response.status_code in [400, 403]:
        logger.warning("The TolaUser {} (id={}) could not be created "
                       "successfully in Track.".format(
                        tolauser.name, tolauser.id))
    return response
