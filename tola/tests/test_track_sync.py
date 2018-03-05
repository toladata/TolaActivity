# -*- coding: utf-8 -*-
import json
import logging

from django.test import RequestFactory, TestCase, override_settings
from mock import Mock, patch

import factories
from tola.track_sync import (register_user, create_instance, update_instance,
                             delete_instance, validate_response)


class ValidateResponseTest(TestCase):
    def test_validate_good_response(self):
        response = Mock(status_code=200)
        wflvl1 = factories.WorkflowLevel1(name='Some name')
        validate_response(response, wflvl1)

    def test_validate_good_response_utf8_object(self):
        response = Mock(status_code=200)
        logging.basicConfig(level=logging.DEBUG )
        wflvl1 = factories.WorkflowLevel1(name=u'色は匂へど 散りぬるを')
        validate_response(response, wflvl1)

    def test_validate_bad_response(self):
        response = Mock(status_code=400)
        wflvl1 = factories.WorkflowLevel1(name='Some name')
        validate_response(response, wflvl1)

    def test_validate_bad_response_utf8_object(self):
        response = Mock(status_code=200)
        logging.basicConfig(level=logging.DEBUG )
        wflvl1 = factories.WorkflowLevel1(name=u'色は匂へど 散りぬるを')
        validate_response(response, wflvl1)


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


class TrackInstanceTest(TestCase):
    def setUp(self):
        logging.disable(logging.WARNING)
        factories.Group()
        self.tola_user = factories.TolaUser()

    def tearDown(self):
        logging.disable(logging.NOTSET)

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('tola.track_sync.logger')
    @patch('tola.track_sync.requests')
    def test_response_org_create(self, mock_requests, mock_logger):
        mock_requests.post.return_value = Mock(status_code=201)

        org = factories.Organization()

        response = create_instance(org)
        self.assertEqual(response.status_code, 201)
        mock_logger.info.assert_called_once_with(
            'The request for {} (id={}, model={}) was successfully executed '
            'on Track.'.format(org.name, org.id, 'Organization'))

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('tola.track_sync.logger')
    @patch('tola.track_sync.requests')
    def test_response_wfl1_create(self, mock_requests, mock_logger):
        content = [{'id': self.tola_user.organization.id}]
        mock_requests.post.return_value = Mock(status_code=201)
        mock_requests.get.return_value = Mock(status_code=200,
                                              content=json.dumps(content))

        wfl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)

        response = create_instance(wfl1)
        self.assertEqual(response.status_code, 201)
        mock_logger.info.assert_called_once_with(
            'The request for {} (id={}, model={}) was successfully executed '
            'on Track.'.format(wfl1.name, wfl1.id, 'WorkflowLevel1'))

    def test_response_wrong_model_create(self):
        tola_user = factories.TolaUser()

        with self.assertRaises(ValueError):
            create_instance(tola_user)

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('tola.track_sync.logger')
    @patch('tola.track_sync.requests')
    def test_response_forbidden(self, mock_requests, mock_logger):
        mock_requests.post.return_value = Mock(status_code=403)

        org = factories.Organization()

        response = create_instance(org)
        self.assertEqual(response.status_code, 403)
        mock_logger.warning.assert_called_once_with(
            '{} (id={}, model={}) could not be created/fetched successfully '
            'on/from Track.'.format(org.name, org.id, 'Organization'))

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('tola.track_sync.logger')
    @patch('tola.track_sync.requests')
    def test_response_org_update(self, mock_requests, mock_logger):
        mock_requests.put.return_value = Mock(status_code=200)

        org = factories.Organization()
        org.name = 'Another Org'
        org.description = 'The Org name was changed'
        org.save()

        response = update_instance(org)
        self.assertEqual(response.status_code, 200)
        mock_logger.info.assert_called_once_with(
            'The request for {} (id={}, model={}) was successfully executed '
            'on Track.'.format(org.name, org.id, 'Organization'))

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('tola.track_sync.logger')
    @patch('tola.track_sync.requests')
    def test_response_wfl1_update(self, mock_requests, mock_logger):
        content = [{'id': self.tola_user.organization.id}]
        mock_requests.put.return_value = Mock(status_code=200)
        mock_requests.get.return_value = Mock(status_code=200,
                                              content=json.dumps(content))

        wfl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wfl1.name = 'Another Org'
        wfl1.save()

        response = update_instance(wfl1)
        self.assertEqual(response.status_code, 200)
        mock_logger.info.assert_called_once_with(
            'The request for {} (id={}, model={}) was successfully executed '
            'on Track.'.format(wfl1.name, wfl1.id, 'WorkflowLevel1'))

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('tola.track_sync.logger')
    @patch('tola.track_sync.requests')
    def test_response_forbidden(self, mock_requests, mock_logger):
        mock_requests.put.return_value = Mock(status_code=403)

        org = factories.Organization()
        org.name = 'Another Org'
        org.description = 'The Org name was changed'
        org.save()

        response = update_instance(org)
        self.assertEqual(response.status_code, 403)
        mock_logger.warning.assert_called_once_with(
            '{} (id={}, model={}) could not be created/fetched successfully '
            'on/from Track.'.format(org.name, org.id, 'Organization'))

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('tola.track_sync.logger')
    @patch('tola.track_sync.requests')
    def test_response_200_delete(self, mock_requests, mock_logger):
        mock_requests.delete.return_value = Mock(status_code=200)

        org = factories.Organization()

        response = delete_instance(org)
        self.assertEqual(response.status_code, 200)
        mock_logger.info.assert_called_once_with(
            'The request for {} (id={}, model={}) was successfully executed '
            'on Track.'.format(org.name, org.id, 'Organization'))

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('tola.track_sync.logger')
    @patch('tola.track_sync.requests')
    def test_response_forbidden(self, mock_requests, mock_logger):
        mock_requests.delete.return_value = Mock(status_code=403)

        org = factories.Organization()

        response = delete_instance(org)
        self.assertEqual(response.status_code, 403)
        mock_logger.warning.assert_called_once_with(
            '{} (id={}, model={}) could not be created/fetched successfully '
            'on/from Track.'.format(org.name, org.id, 'Organization'))
