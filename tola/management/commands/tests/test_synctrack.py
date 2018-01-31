import logging
import sys
import json

from django.core.management import call_command
from django.test import TestCase, override_settings, tag

from mock import Mock, patch

import factories
from tola.management.commands.synctrack import Command


class DevNull(object):
    def write(self, data):
        pass


class SyncTrackTest(TestCase):
    def setUp(self):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        sys.stdout = DevNull()
        sys.stderr = DevNull()
        logging.disable(logging.ERROR)

        self.org = factories.Organization()
        self.wfl1 = factories.WorkflowLevel1(organization=self.org)

    def tearDown(self):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        logging.disable(logging.NOTSET)

    @patch('tola.management.commands.synctrack.requests')
    def test_sync_track(self, mock_requests):
        mock_requests.get.return_value = Mock(status_code=200, content='[]')
        mock_requests.put.return_value = Mock(status_code=200)
        mock_requests.post.return_value = Mock(status_code=201,
                                               content='{"id": 1}')

        args = []
        opts = {}
        call_command('synctrack', *args, **opts)

    @override_settings(TOLA_TRACK_TOKEN='')
    def test_get_headers_no_token(self):
        command = Command()
        headers = command._get_headers()
        self.assertNotIn('Authorization', headers)

    @override_settings(TOLA_TRACK_TOKEN='The Token')
    def test_get_headers_token(self):
        command = Command()
        headers = command._get_headers()
        self.assertIn('Authorization', headers)

    @patch('tola.management.commands.synctrack.requests')
    def test_check_instance_no_org(self, mock_requests):
        mock_requests.get.return_value = Mock(status_code=200, content='[]')
        mock_requests.post.return_value = Mock(status_code=201,
                                               content='{"id": 1}')
        command = Command()
        instance_id = command._check_instance('organization', self.org.name)
        self.assertEqual(instance_id, '1')

    @patch('tola.management.commands.synctrack.requests')
    def test_check_instance_org(self, mock_requests):
        mock_requests.get.return_value = Mock(status_code=200,
                                              content='[{"id": 2}]')
        command = Command()
        instance_id = command._check_instance('organization', self.org.name)
        self.assertEqual(instance_id, '2')

    @patch('tola.management.commands.synctrack.requests')
    def test_request_to_track_no_org(self, mock_requests):
        mock_requests.put.return_value = Mock(status_code=404)
        mock_requests.post.return_value = Mock(status_code=201,
                                               content='{"id": 3}')
        command = Command()
        payload = {
            'name': self.org.name,
        }
        response = command._request_to_track('organization', payload,
                                             self.org.id)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(content['id'], 3)

    @patch('tola.management.commands.synctrack.requests')
    def test_request_to_track_org(self, mock_requests):
        mock_requests.put.return_value = Mock(status_code=200,
                                              content='{"id": 4}')
        command = Command()
        payload = {
            'name': self.org.name,
        }
        response = command._request_to_track('organization', payload,
                                             self.org.id)
        content = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(content['id'], 4)

    def test_save_wfl1(self):
        Command._check_instance = Mock()
        Command._request_to_track = Mock()

        command = Command()
        result = command.save_wfl1()
        self.assertIn(str(self.wfl1.id), result)

    def test_save_org(self):
        Command._check_instance = Mock()
        Command._request_to_track = Mock()

        command = Command()
        result = command.save_org()
        self.assertIn(str(self.org.id), result)
