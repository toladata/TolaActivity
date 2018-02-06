import logging
import sys

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
        self.wfl2 = factories.WorkflowLevel2(workflowlevel1=self.wfl1)

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
    def test_get_from_track_no_org(self, mock_requests):
        mock_requests.get.return_value = Mock(status_code=200, content='[{}]')
        mock_requests.post.return_value = Mock(status_code=201,
                                               content='{"id": 1}')
        command = Command()
        data = command._get_from_track('organization', self.org.name)
        self.assertEqual(data, {})

    @patch('tola.management.commands.synctrack.requests')
    def test_get_from_track_org(self, mock_requests):
        mock_requests.get.return_value = Mock(status_code=200,
                                              content='[{"id": 2}]')
        command = Command()
        data = command._get_from_track('organization', self.org.name)
        self.assertEqual(data['id'], 2)

    @patch('tola.management.commands.synctrack.Command._get_from_track')
    @patch('tola.management.commands.synctrack.requests')
    def test_create_or_update_no_org(self, mock_requests, mock_get_from_track):
        mock_get_from_track.return_value = {}
        mock_requests.post.return_value = Mock(status_code=201,
                                               content='{"id": 3}')
        command = Command()
        payload = {
            'name': self.org.name,
        }
        result = command._create_or_update('organization', self.org.id, payload)
        self.assertEqual(result, '3')

    @patch('tola.management.commands.synctrack.Command._get_from_track')
    @patch('tola.management.commands.synctrack.requests')
    def test_create_or_update_with_org(self, mock_requests,
                                       mock_get_from_track):
        mock_get_from_track.return_value = {'id': 4}
        mock_requests.put.return_value = Mock(status_code=200,
                                              content='{"id": 4}')
        command = Command()
        payload = {
            'name': self.org.name,
        }
        result = command._create_or_update('organization', self.org.id, payload)
        self.assertEqual(result, '4')

    @patch('tola.management.commands.synctrack.Command._get_from_track')
    @patch('tola.management.commands.synctrack.requests')
    def test_create_or_update_failed(self, mock_requests, mock_get_from_track):
        mock_get_from_track.return_value = {'id': 4}
        mock_requests.put.return_value = Mock(status_code=404)
        command = Command()
        payload = {
            'name': self.org.name,
        }
        result = command._create_or_update('organization', self.org.id, payload)
        self.assertEqual(result, None)

    @patch('tola.management.commands.synctrack.Command._get_from_track')
    @patch('tola.management.commands.synctrack.Command._create_or_update')
    def test_save_wfl2(self, mock_create_or_update, mock_get_from_track):
        mock_create_or_update.return_value = self.wfl2.id
        mock_get_from_track.return_value = {'id': self.wfl2.id}

        command = Command()
        result = command.save_wfl2()
        self.assertIn(self.wfl2.id, result)

    @patch('tola.management.commands.synctrack.Command._get_from_track')
    @patch('tola.management.commands.synctrack.Command._create_or_update')
    def test_save_wfl1(self, mock_create_or_update, mock_get_from_track):
        mock_create_or_update.return_value = self.wfl1.id
        mock_get_from_track.return_value = {'id': self.wfl1.id}

        command = Command()
        result = command.save_wfl1()
        self.assertIn(self.wfl1.id, result)

    @patch('tola.management.commands.synctrack.Command._create_or_update')
    def test_save_org(self, mock_create_or_update):
        mock_create_or_update.return_value = self.org.id

        command = Command()
        result = command.save_org()
        self.assertIn(self.org.id, result)
