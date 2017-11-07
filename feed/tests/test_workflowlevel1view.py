from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import WorkflowLevel1ViewSet
from workflow.models import (WorkflowTeam, WorkflowLevel1,
                             ROLE_ORGANIZATION_ADMIN, ROLE_PROGRAM_TEAM,
                             ROLE_PROGRAM_ADMIN)


class WorkflowLevel1ViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        factories.Group()

    def test_list_workflowlevel1_superuser(self):
        wflvl1 = factories.WorkflowLevel1()
        wflvl2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)

        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.get('/api/workflowlevel1/')
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], wflvl1.name)
        self.assertEqual(response.data[0]['budget'],
                         wflvl2.total_estimated_budget)
        self.assertEqual(response.data[0]['actuals'], wflvl2.actual_cost)

    def test_list_workflowlevel1_org_admin(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user, workflowlevel1=wflvl1,
            role=group_org_admin)

        request = self.factory.get('/api/workflowlevel1/')
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], wflvl1.name)
        self.assertEqual(response.data[0]['budget'],
                         wflvl2.total_estimated_budget)
        self.assertEqual(response.data[0]['actuals'], wflvl2.actual_cost)

    def test_list_workflowlevel1_program_admin(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)
        group_program_admin = factories.Group(name=ROLE_PROGRAM_ADMIN)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user, workflowlevel1=wflvl1,
            role=group_program_admin)

        request = self.factory.get('/api/workflowlevel1/')
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], wflvl1.name)
        self.assertEqual(response.data[0]['budget'],
                         wflvl2.total_estimated_budget)
        self.assertEqual(response.data[0]['actuals'], wflvl2.actual_cost)

    def test_list_workflowlevel1_program_team(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)
        group_program_team = factories.Group(name=ROLE_PROGRAM_TEAM)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user, workflowlevel1=wflvl1,
            role=group_program_team)

        request = self.factory.get('/api/workflowlevel1/')
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], wflvl1.name)
        self.assertEqual(response.data[0]['budget'],
                         wflvl2.total_estimated_budget)
        self.assertEqual(response.data[0]['actuals'], wflvl2.actual_cost)

    def test_list_workflowlevel1_normal_user_same_org(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)

        request = self.factory.get('/api/workflowlevel1/')
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_create_workflowlevel1(self):
        data = {'name': 'Save the Children'}
        request = self.factory.post('/api/workflowlevel1/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Save the Children')

        wft = WorkflowTeam.objects.get(workflowlevel1__id=response.data['id'])
        self.assertEqual(wft.workflow_user, self.tola_user)

        wflvl1 = WorkflowLevel1.objects.get(pk=response.data['id'])
        self.assertEqual(wflvl1.organization, self.tola_user.organization)
        self.assertEqual(wflvl1.user_access.all().count(), 1)
        self.assertEqual(wflvl1.user_access.first(), self.tola_user)

    def test_update_unexisting_workflowlevel1(self):
        data = {'name': 'Save the Lennons'}
        request = self.factory.post('/api/workflowlevel1/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'post': 'update'})
        response = view(request, pk=288)
        self.assertEqual(response.status_code, 404)

    def test_update_workflowlevel1_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        wflvl1 = factories.WorkflowLevel1()
        data = {'name': 'Save the Lennons'}
        request = self.factory.post('/api/workflowlevel1/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'post': 'update'})
        response = view(request, pk=wflvl1.pk)
        self.assertEqual(response.status_code, 200)

        wflvl1 = WorkflowLevel1.objects.get(pk=response.data['id'])
        self.assertEquals(wflvl1.name, data['name'])

    def test_update_workflowlevel1_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        data = {'name': 'Save the Lennons'}
        request = self.factory.post('/api/workflowlevel1/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'post': 'update'})
        response = view(request, pk=wflvl1.pk)
        self.assertEqual(response.status_code, 200)

        wflvl1 = WorkflowLevel1.objects.get(pk=response.data['id'])
        self.assertEquals(wflvl1.name, data['name'])

    def test_update_workflowlevel1_different_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        wflvl1 = factories.WorkflowLevel1(
            organization=factories.Organization(name='Other Org'))
        data = {'name': 'Save the Lennons'}
        request = self.factory.post('/api/workflowlevel1/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'post': 'update'})
        response = view(request, pk=wflvl1.pk)
        self.assertEqual(response.status_code, 403)

    def test_update_workflowlevel1_program_admin(self):
        data = {'name': 'Save the Children'}
        request = self.factory.post('/api/workflowlevel1/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'post': 'create'})
        response = view(request)

        data = {'name': 'Save the Lennons'}
        request = self.factory.post('/api/workflowlevel1/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'post': 'update'})
        response = view(request, pk=response.data['id'])
        self.assertEqual(response.status_code, 200)

        wflvl1 = WorkflowLevel1.objects.get(pk=response.data['id'])
        self.assertEquals(wflvl1.name, data['name'])

    def test_update_workflowlevel1_program_team(self):
        wflvl1 = factories.WorkflowLevel1()
        group_program_team = factories.Group(name=ROLE_PROGRAM_TEAM)
        wflvl1.organization = self.tola_user.organization
        wflvl1.user_access.add(self.tola_user)
        wflvl1.save()
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user, workflowlevel1=wflvl1,
            role=group_program_team)

        data = {'name': 'Save the Lennons'}
        request = self.factory.post('/api/workflowlevel1/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'post': 'update'})
        response = view(request, pk=wflvl1.pk)
        self.assertEqual(response.status_code, 200)

        wflvl1 = WorkflowLevel1.objects.get(pk=response.data['id'])
        self.assertEquals(wflvl1.name, data['name'])

    def test_update_workflowlevel1_same_org_different_program_team(self):
        wflvl1_other = factories.WorkflowLevel1()
        group_program_team = factories.Group(name=ROLE_PROGRAM_TEAM)
        wflvl1_other.organization = self.tola_user.organization
        wflvl1_other.user_access.add(self.tola_user)
        wflvl1_other.save()
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user, workflowlevel1=wflvl1_other,
            role=group_program_team)

        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)

        data = {'name': 'Save the Lennons'}
        request = self.factory.post('/api/workflowlevel1/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'post': 'update'})
        response = view(request, pk=wflvl1.pk)
        self.assertEqual(response.status_code, 403)

    def test_delete_workflowlevel1_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        wflvl1 = factories.WorkflowLevel1()
        request = self.factory.delete('/api/workflowlevel1/')
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=wflvl1.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            WorkflowLevel1.DoesNotExist,
            WorkflowLevel1.objects.get, pk=wflvl1.pk)

    def test_delete_workflowlevel1_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        request = self.factory.delete('/api/workflowlevel1/')
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=wflvl1.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            WorkflowLevel1.DoesNotExist,
            WorkflowLevel1.objects.get, pk=wflvl1.pk)

    def test_delete_workflowlevel1_different_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        org_other = factories.Organization(name='Other Org')
        wflvl1 = factories.WorkflowLevel1(organization=org_other)
        request = self.factory.delete('/api/workflowlevel1/')
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=wflvl1.pk)
        self.assertEquals(response.status_code, 403)
        WorkflowLevel1.objects.get(pk=wflvl1.pk)

    def test_delete_workflowlevel1_program_admin(self):
        # Create a program
        data = {'name': 'Save the Children'}
        request = self.factory.post('/api/workflowlevel1/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)

        # Delete the program created before
        request = self.factory.delete('/api/workflowlevel1/')
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'delete': 'destroy'})
        view(request, pk=response.data['id'])
        self.assertRaises(
            WorkflowLevel1.DoesNotExist,
            WorkflowLevel1.objects.get, pk=response.data['id'])

    def test_delete_workflowlevel1_different_org(self):
        group_other = factories.Group(name='other')
        self.tola_user.user.groups.add(group_other)

        wflvl1 = factories.WorkflowLevel1()
        request = self.factory.delete('/api/workflowlevel1/')
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=wflvl1.pk)
        self.assertEquals(response.status_code, 403)
        WorkflowLevel1.objects.get(pk=wflvl1.pk)

    def test_delete_workflowlevel1_normal_user(self):
        wflvl1 = factories.WorkflowLevel1()
        request = self.factory.delete('/api/workflowlevel1/')
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=wflvl1.pk)
        self.assertEquals(response.status_code, 403)
        WorkflowLevel1.objects.get(pk=wflvl1.pk)

    def test_delete_workflowlevel1_program_admin_just_one(self):
        # Create a program
        data = {'name': 'Save the Pandas'}
        request = self.factory.post('/api/workflowlevel1/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'post': 'create'})
        response = view(request)
        first_program_id = response.data['id']

        # Create another program
        data = {'name': 'Save the Children'}
        request = self.factory.post('/api/workflowlevel1/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'post': 'create'})
        response = view(request)

        # Delete only the latter program
        request = self.factory.delete('/api/workflowlevel1/')
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'delete': 'destroy'})
        view(request, pk=response.data['id'])
        self.assertRaises(
            WorkflowLevel1.DoesNotExist,
            WorkflowLevel1.objects.get, pk=response.data['id'])
        WorkflowLevel1.objects.get(pk=first_program_id)
