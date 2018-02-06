import json
import requests
import logging
import sys
import random
from urlparse import urljoin

from django.core.management.base import BaseCommand
from django.conf import settings

from workflow.models import (Organization, TolaUser, WorkflowLevel1,
                             WorkflowLevel2)
from tola.track_sync import register_user

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

    def _get_from_track(self, section, params):
        """
        Get the instance ID from Track based on the name
        :param section:
        :param name:
        :return: the Track instance id
        """
        headers = self._get_headers()
        list_params = ['{}={}'.format(k, v) for k, v in params.iteritems()]
        query_params = '&'.join(list_params)
        url_subpath = 'api/{}?format=json&{}'.format(section, query_params)
        url = urljoin(settings.TOLA_TRACK_URL, url_subpath)
        response = requests.get(url, headers=headers, verify=False)
        data = json.loads(response.content)
        if data:
            return data[0]

    def _create_or_update(self, section, params, payload):
        """
        Create or update the instance in Track
        :param section:
        :param params:
        :param payload:
        :return: the Track instance id
        """
        instance_id = None
        headers = self._get_headers()
        data = self._get_from_track(section, params)
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
            params = {
                'organization_uuid': program.organization.organization_uuid
            }
            data = self._get_from_track('organization', params)
            org_id = data['id']

            # set payload and deliver
            payload = {
                'level1_uuid': program.level1_uuid,
                'name': program.name,
                'organization': org_id,
            }
            wfl1_id = self._create_or_update('workflowlevel1', params, payload)

            updated_wfl1s.append(str(wfl1_id))
        sys.stdout.write('\n')
        return updated_wfl1s

    def save_wfl2(self):
        """
        Update or create each workflowlevel2 in Track
        """
        # update TolaTrack with program data
        projects = WorkflowLevel2.objects.all()
        updated_wfl2s = []

        # each level2 send to Track
        for project in projects:
            sys.stdout.write('.')
            params = {
                'level1_uuid': project.workflowlevel1.level1_uuid
            }
            data = self._get_from_track('workflowlevel1', params)
            wfl1_id = data['id']

            # set payload and deliver
            payload = {
                'level2_uuid': project.level2_uuid,
                'name': project.name,
                'workflowlevel1': wfl1_id,
            }

            self._create_or_update('workflowlevel2', params, payload)
            updated_wfl2s.append(str(project.id))
        sys.stdout.write('\n')
        return updated_wfl2s

    def save_tola_user(self):
        """
        Update or create each Tola User in Track
        """
        # update TolaTrack with program data
        tola_users = TolaUser.objects.all()
        updated_tola_users = []

        # each tola user send to Track
        for tola_user in tola_users:
            sys.stdout.write('.')
            params = {
                'organization_uuid': tola_user.organization.organization_uuid
            }
            data = self._get_from_track('organization', params)
            org_id = data['id']
            org_name = data['name']

            # set payload and deliver
            payload = {
                'title': tola_user.title,
                'tola_user_uuid': tola_user.tola_user_uuid
            }

            params = {
                'tola_user_uuid': tola_user.tola_user_uuid
            }
            data = self._get_from_track('tolauser', params)
            if not data:
                generated_pass = '%032x' % random.getrandbits(128)
                create_data = {
                    'username': tola_user.user.username,
                    'first_name': tola_user.user.first_name,
                    'last_name': tola_user.user.last_name,
                    'email': tola_user.user.email,
                    'password1': generated_pass,
                    'password2': generated_pass,
                    'org': org_name
                }
                payload.update(create_data)
                register_user(payload, tola_user)
            else:
                update_data = {
                    'name': tola_user.name,
                    'organization': org_id,
                }
                payload.update(update_data)
                self._create_or_update('tolauser', params, payload)
            updated_tola_users.append(str(tola_user.id))

        sys.stdout.write('\n')
        return updated_tola_users

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
            params = {
                'organization_uuid': org.organization_uuid
            }
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
            org_id = self._create_or_update('organization', params, payload)
            updated_orgs.append(str(org_id))
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

        sys.stdout.write('INFO: Syncing Tola Users')
        try:
            result = self.save_tola_user()
            tolauser_ids = ', '.join(result)
            logger.info('The id of updated tola users: {}'.format(tolauser_ids))
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

