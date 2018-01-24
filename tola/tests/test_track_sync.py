import json
import logging

from django.test import RequestFactory, TestCase, override_settings
from mock import Mock, patch

import factories
from tola.track_sync import register_user, create_workflowlevel1


class RegisterUserTest(TestCase):
    def setUp(self):
        logging.disable(logging.WARNING)
        factories.Group()
        self.tola_user = factories.TolaUser()
        self.factory = RequestFactory()

    def tearDown(self):
        logging.disable(logging.NOTSET)

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('tola.track_sync.requests')
    def test_response_201_create(self, mock_requests):
        external_response = {
            'url': 'http://testserver/api/tolauser/2',
            'tola_user_uuid': 1234567890,
            'name': 'John Lennon',
        }
        mock_requests.post.return_value = Mock(
            status_code=201, content=json.dumps(external_response))

        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        user = factories.User(first_name='John', last_name='Lennon')
        tolauser = factories.TolaUser(user=user, tola_user_uuid=1234567890)
        data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'username': user.username,
            'tola_user_uuid': tolauser.tola_user_uuid
        }

        response = register_user(data, tolauser)
        result = json.loads(response.content)

        self.assertEqual(result['tola_user_uuid'], 1234567890)
        mock_requests.post.assert_called_once_with(
            'https://tolatrack.com/accounts/register/',
            data={'username': 'johnlennon',
                  'first_name': 'John',
                  'last_name': 'Lennon',
                  'tola_user_uuid': tolauser.tola_user_uuid,
                  'email': 'johnlennon@testenv.com'},
            headers={'Authorization': 'Token TheToken'})

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('tola.track_sync.requests')
    def test_response_403_forbidden(self, mock_requests):
        mock_requests.post.return_value = Mock(status_code=403)

        user = factories.User(first_name='John', last_name='Lennon')
        tolauser = factories.TolaUser(user=user)
        data = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'username': user.username,
            'tola_user_uuid': tolauser.tola_user_uuid
        }

        response = register_user(data, tolauser)

        self.assertTrue(isinstance(response.content, Mock))
        mock_requests.post.assert_called_once_with(
            'https://tolatrack.com/accounts/register/',
            data={'username': 'johnlennon',
                  'first_name': 'John',
                  'last_name': 'Lennon',
                  'tola_user_uuid': tolauser.tola_user_uuid,
                  'email': 'johnlennon@testenv.com'},
            headers={'Authorization': 'Token TheToken'})


class CreateWFL1Test(TestCase):
    def setUp(self):
        logging.disable(logging.WARNING)
        factories.Group()
        self.tola_user = factories.TolaUser()
        self.factory = RequestFactory()

    def tearDown(self):
        logging.disable(logging.NOTSET)

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('tola.track_sync.requests')
    def test_response_201_create(self, mock_requests):
        external_response = [{
            'id': self.tola_user.organization.id,
        }]
        mock_requests.get.return_value = Mock(
            status_code=200, content=json.dumps(external_response))
        mock_requests.post.return_value = Mock(status_code=201)

        wfl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)

        response = create_workflowlevel1(wfl1)
        self.assertEqual(response.status_code, 201)

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('tola.track_sync.requests')
    def test_response_no_organization(self, mock_requests):
        mock_requests.get.return_value = Mock(
            status_code=200, content='[]')

        wfl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)

        response = create_workflowlevel1(wfl1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '[]')

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('tola.track_sync.requests')
    def test_response_bad_request(self, mock_requests):
        mock_requests.get.return_value = Mock(status_code=400)

        wfl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)

        response = create_workflowlevel1(wfl1)
        self.assertEqual(response.status_code, 400)
