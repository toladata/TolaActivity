import json
import requests
import uuid
import logging
import sys
from urlparse import urljoin

from django.core.management.base import BaseCommand
from django.conf import settings

from workflow.models import Organization, WorkflowLevel1

logger = logging.getLogger(__name__)

# TODO: We need to implement a check for programs and orgs that are in Track
# TODO: but they don't exist anymore in Activity


class Command(BaseCommand):
    help = 'Synchronizes data by pushing it from Activity to Track'

    def _get_headers(self):
        """
        Authentication for Track
        Get the header information to send to Track in the request
        :return: headers
        """
        if settings.TOLA_TRACK_TOKEN:
            headers = {
                'content-type': 'application/json',
                'Authorization': 'Token {}'.format(settings.TOLA_TRACK_TOKEN)
            }
        else:
            headers = {'content-type': 'application/json'}
            logger.warn('Token Not Found')

        return headers

    def _request_to_track(self, section, payload, id):
        """
        send the requests to individual API endpoint in Track
        with the payload and id
        :param section: model class on Track and activity
        :return: status: success of failure of request
        """
        headers = self._get_headers()

        # Try to update if there is an instance in Track
        url_subpath = 'api/{}/{}'.format(section, id)
        put_url = urljoin(settings.TOLA_TRACK_URL, url_subpath)
        response = requests.put(put_url, json=payload, headers=headers,
                                verify=False)

        if response.status_code == 404:
            post_url = urljoin(settings.TOLA_TRACK_URL,
                               'api/{}'.format(section))
            response = requests.post(post_url, json=payload, headers=headers,
                                     verify=False)

        return response

    def _check_instance(self, section, name):
        """
        Get or create the instance in Track
        :param section:
        :param name:
        :return: the Track instance id
        """
        headers = self._get_headers()

        # Check if there is an instance in Track
        url_subpath = 'api/{}?format=json&name={}'.format(section, name)
        check_url = urljoin(settings.TOLA_TRACK_URL, url_subpath)
        check_resp = requests.get(check_url, headers=headers, verify=False)
        data = json.loads(check_resp.content)

        # If there is no instance in Track, we'll create it
        if not data:
            post_url = urljoin(settings.TOLA_TRACK_URL,
                               'api/{}'.format(section))
            payload = {}
            if section == 'organization':
                payload = {
                    'name': name,
                }
            elif section == 'workflowlevel1':
                payload = {
                    'level1_uuid': uuid.uuid4().__str__(),
                    'name': name,
                }
            post_resp = requests.post(post_url, json=payload, headers=headers,
                                      verify=False)
            # get data response from post
            data = [json.loads(post_resp.content)]

        instance_id = str(data[0]['id'])
        return instance_id

    def save_wfl1(self):
        """
        Update or create each workflowlevel1 in Track
        """
        # update TolaTrack with program data
        programs = WorkflowLevel1.objects.all()
        updated_wfl1s = []

        # each level1 send to Track
        for program in programs:
            sys.stdout.write('.')
            org_id = self._check_instance('organization',
                                         program.organization.name)

            # set payload and deliver
            payload = {
                'level1_uuid': program.level1_uuid,
                'name': program.name,
                'organization': org_id,
            }

            self._request_to_track(section='workflowlevel1',
                                   payload=payload,
                                   id=program.id)
            updated_wfl1s.append(program.id)
        sys.stdout.write('\n')
        return updated_wfl1s

    def save_org(self):
        """
        Update or create each organization in Track
        """
        # update TolaTrack with program data
        orgs = Organization.objects.all()
        updated_orgs = []

        # each level1 send to Track
        for org in orgs:
            sys.stdout.write('.')
            org_id = self._check_instance('organization', org.name)

            # set payload and send to Track
            payload = {
                'organization_uuid': org.organization_uuid,
                'name': org.name,
                'description': org.description,
                'organization_url': org.organization_url,
                'level_1_label': org.level_1_label,
                'level_2_label': org.level_2_label,
                'level_3_label': org.level_3_label,
                'level_4_label': org.level_4_label,
            }
            self._request_to_track(section='organization',
                                   payload=payload,
                                   id=org_id)
            updated_orgs.append(org.id)
        sys.stdout.write('\n')
        return updated_orgs

    def handle(self, *args, **options):
        sys.stdout.write('INFO: Starting the sync process\n')

        sys.stdout.write('INFO: Syncing Organizations')
        try:
            result = self.save_org()
            org_ids = ', '.join(result)
            logger.info('The id of updated organizations: {}'.format(org_ids))
        except Exception as e:
            logger.error(e)

        sys.stdout.write('INFO: Syncing WorkflowLevels1')
        try:
            result = self.save_wfl1()
            wfl1_ids = ', '.join(result)
            logger.info('The id of updated programs: {}'.format(wfl1_ids))
        except Exception as e:
            logger.error(e)
