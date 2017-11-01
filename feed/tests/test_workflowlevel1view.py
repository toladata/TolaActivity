from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import WorkflowLevel1ViewSet
from workflow.models import WorkflowTeam, WorkflowLevel1, ROLE_ORGANIZATION_ADMIN


class WorkflowLevel1ViewsTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()
        factories.Group()

    def test_create_workflowlevel1(self):
        factory = APIRequestFactory()
        data = {'name': 'Save the Children'}
        request = factory.post('/api/workflowlevel1/', data)
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

    def test_delete_workflowlevel1_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        wflvl1 = factories.WorkflowLevel1()
        factory = APIRequestFactory()
        request = factory.delete('/api/workflowlevel1/')
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

        wflvl1 = factories.WorkflowLevel1()
        factory = APIRequestFactory()
        request = factory.delete('/api/workflowlevel1/')
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=wflvl1.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            WorkflowLevel1.DoesNotExist,
            WorkflowLevel1.objects.get, pk=wflvl1.pk)

    def test_delete_workflowlevel1_program_admin(self):
        # Create a program
        factory = APIRequestFactory()
        data = {'name': 'Save the Children'}
        request = factory.post('/api/workflowlevel1/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)

        # Delete the program created before
        factory = APIRequestFactory()
        request = factory.delete('/api/workflowlevel1/')
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'delete': 'destroy'})
        view(request, pk=response.data['id'])
        self.assertRaises(
            WorkflowLevel1.DoesNotExist,
            WorkflowLevel1.objects.get, pk=response.data['id'])

    def test_delete_workflowlevel1_different_org_admin(self):
        group_other = factories.Group(name='other')
        self.tola_user.user.groups.add(group_other)

        wflvl1 = factories.WorkflowLevel1()
        factory = APIRequestFactory()
        request = factory.delete('/api/workflowlevel1/')
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=wflvl1.pk)
        self.assertEquals(response.status_code, 403)
        WorkflowLevel1.objects.get(pk=wflvl1.pk)

    def test_delete_workflowlevel1_normal_user(self):
        wflvl1 = factories.WorkflowLevel1()
        factory = APIRequestFactory()
        request = factory.delete('/api/workflowlevel1/')
        request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=wflvl1.pk)
        self.assertEquals(response.status_code, 403)
        WorkflowLevel1.objects.get(pk=wflvl1.pk)
