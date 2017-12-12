import json

from django.test import TestCase, override_settings
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

from mock import Mock, patch

import factories
from feed.views import CustomFormViewSet
from formlibrary.models import CustomForm
from workflow.models import (WorkflowLevel1, WorkflowTeam,
                             ROLE_ORGANIZATION_ADMIN, ROLE_PROGRAM_TEAM,
                             ROLE_PROGRAM_ADMIN, ROLE_VIEW_ONLY)


class CustomFormListViewsTest(TestCase):
    def setUp(self):
        factories.Organization(id=1)
        factories.CustomForm.create_batch(2)
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_list_customform_superuser(self):
        request = self.factory.get('/api/customform/')
        request.user = factories.User.build(is_superuser=True,
                                            is_staff=True)
        view = CustomFormViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_customform_org_admin(self):
        request = self.factory.get('/api/customform/')
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.CustomForm(organization=self.tola_user.organization)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_customform_program_admin(self):
        request = self.factory.get('/api/customform/')
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.CustomForm(organization=self.tola_user.organization)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_customform_program_team(self):
        request = self.factory.get('/api/customform/')
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.CustomForm(organization=self.tola_user.organization)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_customform_view_only(self):
        request = self.factory.get('/api/customform/')
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            role=factories.Group(name=ROLE_VIEW_ONLY))
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.CustomForm(organization=self.tola_user.organization)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class CustomFormCreateViewsTest(TestCase):
    def setUp(self):
        org = factories.Organization(id=1)
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser(organization=org)
        factories.Group()

    def test_create_customform_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        data = {'name': '4W Daily Activity Report'}

        request = self.factory.post('/api/customform/', data)
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], '4W Daily Activity Report')

    def test_create_customform_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.post('/api/customform/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': '4W Daily Activity Report',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/customform/', data)
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], '4W Daily Activity Report')

    def test_create_customform_program_admin(self):
        request = self.factory.post('/api/customform/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        data = {'name': '4W Daily Activity Report',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/customform/', data)
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], '4W Daily Activity Report')

    def test_create_customform_program_admin_json(self):
        request = self.factory.post('/api/customform/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        data = {'name': '4W Daily Activity Report',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/customform/', json.dumps(data),
                                    content_type='application/json')
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], '4W Daily Activity Report')

    def test_create_customform_program_team(self):
        request = self.factory.post('/api/customform/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))

        data = {'name': '4W Daily Activity Report',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/customform/', data)
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], '4W Daily Activity Report')

    def test_create_customform_view_only(self):
        request = self.factory.post('/api/customform/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_VIEW_ONLY))

        data = {'name': '4W Daily Activity Report',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/customform/', data)
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 403)


class CustomFormUpdateViewsTest(TestCase):
    def setUp(self):
        org = factories.Organization(id=1)
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser(organization=org)
        factories.Group()

    def test_update_unexisting_customform(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        data = {'name': '4W Daily Activity Report'}
        request = self.factory.post('/api/customform/', data)
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'post': 'update'})
        response = view(request, pk=288)
        self.assertEqual(response.status_code, 404)

    def test_update_customform_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        customform = factories.CustomForm()

        data = {'name': '4W Daily Activity Report'}
        request = self.factory.post('/api/customform/', data)
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'post': 'update'})
        response = view(request, pk=customform.pk)
        self.assertEqual(response.status_code, 200)

        customform = CustomForm.objects.get(pk=response.data['id'])
        self.assertEquals(customform.name, data['name'])

    def test_update_customform_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        customform = factories.CustomForm(
            organization=self.tola_user.organization)

        data = {'name': '4W Daily Activity Report'}
        request = self.factory.post('/api/customform/', data)
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'post': 'update'})
        response = view(request, pk=customform.pk)
        self.assertEqual(response.status_code, 200)

        customform = CustomForm.objects.get(pk=response.data['id'])
        self.assertEquals(customform.name, data['name'])

    def test_update_customform_org_admin_json(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        customform = factories.CustomForm(
            organization=self.tola_user.organization,
            created_by=self.tola_user.user)

        data = {'name': '4W Daily Activity Report'}
        request = self.factory.post('/api/customform/', json.dumps(data),
                                    content_type='application/json')
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'post': 'update'})
        response = view(request, pk=customform.pk)
        self.assertEqual(response.status_code, 200)

        customform = CustomForm.objects.get(pk=response.data['id'])
        self.assertEquals(customform.name, data['name'])

    def test_update_customform_diff_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        another_org = factories.Organization(name='Another Org')
        customform = factories.CustomForm(
            organization=another_org)

        data = {'name': '4W Daily Activity Report'}
        request = self.factory.post('/api/customform/', data)
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'post': 'update'})
        response = view(request, pk=customform.pk)
        self.assertEqual(response.status_code, 403)

    def test_update_customform_no_created_by(self):
        customform = factories.CustomForm(
            organization=self.tola_user.organization)

        data = {'name': '4W Daily Activity Report'}
        request = self.factory.post('/api/customform/', data)
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'post': 'update'})
        response = view(request, pk=customform.pk)
        self.assertEqual(response.status_code, 403)

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('feed.views.requests')
    def test_update_customform_org_admin_first_wfl1(self, mock_requests):
        external_response = {'id': 1234}
        mock_requests.post.return_value = Mock(
            status_code=201, content=json.dumps(external_response))
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.post('/api/customform/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        customform = factories.CustomForm(
            organization=self.tola_user.organization)

        data = {'name': '4W Daily Activity Report',
                'description': 'It is a test',
                'fields': '[{"name": "name", "type": "text"},'
                          '{"name": "age", "type": "number"},'
                          '{"name": "city", "type": "text"}]',
                'workflowlevel1': wflvl1_url}
        request = self.factory.post('/api/customform/', data)
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'post': 'update'})
        response = view(request, pk=customform.pk)
        self.assertEqual(response.status_code, 200)

        customform = CustomForm.objects.get(pk=response.data['id'])
        self.assertEquals(customform.name, data['name'])

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('feed.views.requests')
    def test_update_customform_org_admin_second_wfl1(self, mock_requests):
        external_response = {'id': 1234}
        mock_requests.get.return_value = Mock(
            status_code=200, content=json.dumps('false'))
        mock_requests.put.return_value = Mock(
            status_code=200, content=json.dumps(external_response))
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.post('/api/customform/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        customform = factories.CustomForm(
            workflowlevel1=wflvl1,
            organization=self.tola_user.organization,
            silo_id=1234)

        data = {'name': '4W Daily Activity Report',
                'description': 'It is a test',
                'fields': '[{"name": "name", "type": "text"},'
                          '{"name": "age", "type": "number"},'
                          '{"name": "city", "type": "text"}]',
                'workflowlevel1': wflvl1_url}
        request = self.factory.post('/api/customform/', data)
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'post': 'update'})
        response = view(request, pk=customform.pk)
        self.assertEqual(response.status_code, 200)

        customform = CustomForm.objects.get(pk=response.data['id'])
        self.assertEquals(customform.name, data['name'])

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('feed.views.requests')
    def test_update_customform_org_admin_third_wfl1(self, mock_requests):
        external_response = {'id': 1234}
        mock_requests.get.return_value = Mock(
            status_code=200, content=json.dumps('false'))
        mock_requests.put.return_value = Mock(
            status_code=200, content=json.dumps(external_response))
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        customform = factories.CustomForm(
            workflowlevel1=wflvl1,
            organization=self.tola_user.organization,
            silo_id=1234)

        data = {'name': '4W Daily Activity Report',
                'description': 'It is a test',
                'fields': '[{"name": "name", "type": "text"},'
                          '{"name": "age", "type": "number"},'
                          '{"name": "city", "type": "text"}]'}
        request = self.factory.post('/api/customform/', data)
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'post': 'update'})
        response = view(request, pk=customform.pk)
        self.assertEqual(response.status_code, 200)

        customform = CustomForm.objects.get(pk=response.data['id'])
        self.assertEquals(customform.name, data['name'])

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('feed.views.requests')
    def test_update_customform_org_admin_fourth_wfl1(self, mock_requests):
        external_response = {'id': 1234}
        mock_requests.get.return_value = Mock(
            status_code=200, content=json.dumps('false'))
        mock_requests.put.return_value = Mock(
            status_code=200, content=json.dumps(external_response))
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.post('/api/customform/')
        wflvl1_1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_2 = factories.WorkflowLevel1()
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1_2.id},
                             request=request)
        customform = factories.CustomForm(
            workflowlevel1=wflvl1_1,
            organization=self.tola_user.organization,
            silo_id=1234)

        data = {'name': '4W Daily Activity Report',
                'description': 'It is a test',
                'fields': '[{"name": "name", "type": "text"},'
                          '{"name": "age", "type": "number"},'
                          '{"name": "city", "type": "text"}]',
                'workflowlevel1': wflvl1_url}
        request = self.factory.post('/api/customform/', data)
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'post': 'update'})
        response = view(request, pk=customform.pk)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['detail'],
                         'You cannot change the Program.')

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('feed.views.requests')
    def test_update_customform_org_admin_fifth_wfl1(self, mock_requests):
        mock_requests.get.return_value = Mock(
            status_code=200, content=json.dumps('true'))
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.post('/api/customform/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        customform = factories.CustomForm(
            workflowlevel1=wflvl1,
            organization=self.tola_user.organization,
            silo_id=1234)

        data = {'name': '4W Daily Activity Report',
                'description': 'It is a test',
                'fields': '[{"name": "name", "type": "text"},'
                          '{"name": "age", "type": "number"},'
                          '{"name": "city", "type": "text"}]',
                'workflowlevel1': wflvl1_url}
        request = self.factory.post('/api/customform/', data)
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'post': 'update'})
        response = view(request, pk=customform.pk)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.data['detail'],
                         'You already have data in the instance.')

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @patch('feed.views.requests')
    def test_update_customform_wfl1_program_admin(self, mock_requests):
        # Mock request
        external_response = {'id': 1234}
        mock_requests.post.return_value = Mock(
            status_code=201, content=json.dumps(external_response))

        # Create a program and program team for the user
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        customform = factories.CustomForm(
            organization=self.tola_user.organization,
            created_by=self.tola_user.user)

        # Make the request
        request = self.factory.post('/api/customform/')
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': '4W Daily Activity Report',
                'workflowlevel1': wflvl1_url}
        request = self.factory.post('/api/customform/', data)
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'post': 'update'})
        response = view(request, pk=customform.pk)
        self.assertEqual(response.status_code, 200)

        customform = CustomForm.objects.get(pk=response.data['id'])
        self.assertEquals(customform.name, data['name'])

    def test_update_customform_wfl1_view_only(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_VIEW_ONLY))
        customform = factories.CustomForm(
            organization=self.tola_user.organization,
            created_by=self.tola_user.user)

        request = self.factory.post('/api/customform/')
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': '4W Daily Activity Report',
                'workflowlevel1': wflvl1_url}
        request = self.factory.post('/api/customform/', data)
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'post': 'update'})
        response = view(request, pk=customform.pk)
        self.assertEqual(response.status_code, 403)


class CustomFormDeleteViewsTest(TestCase):
    def setUp(self):
        org = factories.Organization(id=1)
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser(organization=org)
        factories.Group()

    def test_delete_customform_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        customform = factories.CustomForm()
        request = self.factory.delete('/api/customform/')
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=customform.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            CustomForm.DoesNotExist,
            CustomForm.objects.get, pk=customform.pk)

    def test_delete_customform_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        customform = factories.CustomForm(
            organization=self.tola_user.organization)
        request = self.factory.delete('/api/customform/')
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=customform.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            CustomForm.DoesNotExist,
            CustomForm.objects.get, pk=customform.pk)

    def test_delete_customform_diff_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        another_org = factories.Organization(name='Another Org')
        customform = factories.CustomForm(organization=another_org)
        request = self.factory.delete('/api/customform/')
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=customform.pk)
        self.assertEquals(response.status_code, 403)
        CustomForm.objects.get(pk=customform.pk)

    def test_delete_customform_created_by(self):
        customform = factories.CustomForm(
            organization=self.tola_user.organization,
            created_by=self.tola_user.user)

        request = self.factory.delete('/api/customform/')
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=customform.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            CustomForm.DoesNotExist,
            CustomForm.objects.get, pk=customform.pk)

    def test_delete_customform_no_created_by(self):
        customform = factories.CustomForm(
            organization=self.tola_user.organization)
        request = self.factory.delete('/api/customform/')
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=customform.pk)
        self.assertEquals(response.status_code, 403)
        CustomForm.objects.get(pk=customform.pk)


class CustomFormFilterViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_filter_customform_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        ext_serv1 = factories.CustomForm(
            organization=self.tola_user.organization)
        factories.CustomForm(name='Custom Form B')
        request = self.factory.get('/api/customform/?organization__id=%s' %
                                   self.tola_user.organization.pk)
        request.user = self.tola_user.user
        view = CustomFormViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], ext_serv1.name)
