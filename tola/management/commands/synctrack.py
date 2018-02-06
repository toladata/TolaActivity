import json
import requests
import logging
import sys
from urlparse import urljoin

from django.core.management.base import BaseCommand
from django.conf import settings

from workflow.models import Organization, WorkflowLevel1, WorkflowLevel2

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

    def _get_from_track(self, section, name):
        """
        Get the instance ID from Track based on the name
        :param section:
        :param name:
        :return: the Track instance id
        """
        headers = self._get_headers()
        url_subpath = 'api/{}?format=json&name={}'.format(section, name)
        url = urljoin(settings.TOLA_TRACK_URL, url_subpath)
        response = requests.get(url, headers=headers, verify=False)
        data = json.loads(response.content)
        return data[0]

    def _create_or_update(self, section, name, payload):
        """
        Create or update the instance in Track
        :param section:
        :param name:
        :param payload:
        :return: the Track instance id
        """
        instance_id = None
        headers = self._get_headers()
        data = self._get_from_track(section, name)
        if data:
            instance_id = data['id']

        # Update if there is an instance in Track, otherwise we'll create one
        if not instance_id:
            url_subpath = 'api/{}'.format(section)
            url = urljoin(settings.TOLA_TRACK_URL, url_subpath)
            response = requests.post(url, json=payload, headers=headers,
                                     verify=False)
        else:
            url_subpath = 'api/{}/{}'.format(section, instance_id)
            url = urljoin(settings.TOLA_TRACK_URL, url_subpath)
            response = requests.put(url, json=payload, headers=headers,
                                    verify=False)

        if response.status_code in [200, 201]:
            data = json.loads(response.content)
            instance_id = str(data['id'])
        else:
            return None
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
            data = self._get_from_track('organization',
                                        program.organization.name)
            org_id = data['id']

            # set payload and deliver
            payload = {
                'level1_uuid': program.level1_uuid,
                'name': program.name,
                'organization': org_id,
            }
            wfl1_id = self._create_or_update('workflowlevel1', program.name,
                                             payload)

            updated_wfl1s.append(wfl1_id)
        sys.stdout.write('\n')
        return updated_wfl1s

    def save_wfl2(self):
        """
        Update or create each workflowlevel2 in Track
        """
        # update TolaTrack with program data
        projects = WorkflowLevel2.objects.all()
        updated_wfl2s = []

        # each level1 send to Track
        for project in projects:
            sys.stdout.write('.')
            data = self._get_from_track('workflowlevel1',
                                        project.workflowlevel1.name)
            wfl1_id = data['id']

            # set payload and deliver
            payload = {
                'level2_uuid': project.level2_uuid,
                'name': project.name,
                'workflowlevel1': wfl1_id,
            }

            self._create_or_update('workflowlevel2', project.name, payload)
            updated_wfl2s.append(project.id)
        sys.stdout.write('\n')
        return updated_wfl2s

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
            org_id = self._create_or_update('organization', org.name, payload)
            updated_orgs.append(org_id)
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

        sys.stdout.write('INFO: Syncing WorkflowLevel1s')
        try:
            result = self.save_wfl1()
            wfl1_ids = ', '.join(result)
            logger.info('The id of updated programs: {}'.format(wfl1_ids))
        except Exception as e:
            logger.error(e)

        sys.stdout.write('INFO: Syncing WorkflowLevel2s')
        try:
            result = self.save_wfl2()
            wfl2_ids = ', '.join(result)
            logger.info('The id of updated projects: {}'.format(wfl2_ids))
        except Exception as e:
            logger.error(e)

