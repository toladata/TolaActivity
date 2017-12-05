from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import json
import factories
from feed.views import WorkflowLevel2SortViewSet
from workflow.models import WorkflowLevel1, WorkflowLevel2Sort, WorkflowTeam, \
    ROLE_ORGANIZATION_ADMIN, ROLE_PROGRAM_TEAM, ROLE_PROGRAM_ADMIN, \
    ROLE_VIEW_ONLY


class WorkflowLevel2SortListViewsTest(TestCase):
    def setUp(self):
        factories.WorkflowLevel2Sort.create_batch(2)
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_list_workflowlevel2sort_superuser(self):
        request = self.factory.get('/api/workflowlevel2sort/')
        request.user = factories.User.build(is_superuser=True,
                                            is_staff=True)
        view = WorkflowLevel2SortViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_workflowlevel2sort_normal_user(self):
        request = self.factory.get('/api/workflowlevel2sort/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1)
        request.user = self.tola_user.user
        view = WorkflowLevel2SortViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.WorkflowLevel2Sort(workflowlevel1=wflvl1)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class WorkflowLevel2SortCreateViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        factories.Group()

    def test_create_workflowlevel2_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.post('/api/workflowlevel2sort/')
        wflvl1 = factories.WorkflowLevel1()
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'workflowlevel2_id': 1,
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/workflowlevel2/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel2SortViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['workflowlevel2_id'], 1)

    def test_create_workflowlevel2sort_normal_user(self):
        request = self.factory.post('/api/workflowlevel2sort/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'workflowlevel2_id': 1,
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/workflowlevel2/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel2SortViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['workflowlevel2_id'], 1)


class WorkflowLevel2SortUpdateViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        factories.Group()

    def test_update_unexisting_workflowlevel2sort(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        data = {'workflowlevel2_id': 1}

        request = self.factory.post('/api/workflowlevel2sort/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel2SortViewSet.as_view({'post': 'update'})
        response = view(request, pk=288)
        self.assertEqual(response.status_code, 404)

    def test_update_workflowlevel2sort_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.post('/api/workflowlevel2sort/')
        wflvl1 = factories.WorkflowLevel1()
        workflowlevel2sort = factories.WorkflowLevel2Sort(workflowlevel1=wflvl1)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'workflowlevel2_id': 1,
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/workflowlevel2sort/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel2SortViewSet.as_view({'post': 'update'})
        response = view(request, pk=workflowlevel2sort.pk)
        self.assertEqual(response.status_code, 200)

        workflowlevel2sort = WorkflowLevel2Sort.objects.get(
            pk=response.data['id'])
        self.assertEquals(workflowlevel2sort.workflowlevel2_id,
                          data['workflowlevel2_id'])

    def test_update_workflowlevel2sort_normal_user(self):
        request = self.factory.post('/api/workflowlevel2sort/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        workflowlevel2sort = factories.WorkflowLevel2Sort(workflowlevel1=wflvl1)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'workflowlevel2_id': 1,
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/workflowlevel2sort/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel2SortViewSet.as_view({'post': 'update'})
        response = view(request, pk=workflowlevel2sort.pk)
        self.assertEqual(response.status_code, 200)

        workflowlevel2sort = WorkflowLevel2Sort.objects.get(
            pk=response.data['id'])
        self.assertEquals(workflowlevel2sort.workflowlevel2_id,
                          data['workflowlevel2_id'])

    def test_update_workflowlevel2sort_diff_org_normal_user(self):
        request = self.factory.post('/api/workflowlevel2sort/')
        another_org = factories.Organization(name='Another Org')
        wflvl1 = factories.WorkflowLevel1(organization=another_org)
        workflowlevel2sort = factories.WorkflowLevel2Sort(workflowlevel1=wflvl1)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'workflowlevel2_id': 1,
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/workflowlevel2sort/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel2SortViewSet.as_view({'post': 'update'})
        response = view(request, pk=workflowlevel2sort.pk)
        self.assertEqual(response.status_code, 403)


class WorkflowLevel2SortDeleteViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        factories.Group()

    def test_delete_workflowlevel2sort_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        workflowlevel2sort = factories.WorkflowLevel2Sort()
        request = self.factory.delete('/api/workflowlevel2sort/')
        request.user = self.tola_user.user
        view = WorkflowLevel2SortViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=workflowlevel2sort.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            WorkflowLevel2Sort.DoesNotExist,
            WorkflowLevel2Sort.objects.get, pk=workflowlevel2sort.pk)

    def test_delete_workflowlevel2sort_normal_user(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        workflowlevel2sort = factories.WorkflowLevel2Sort(workflowlevel1=wflvl1)

        request = self.factory.delete('/api/workflowlevel2sort/')
        request.user = self.tola_user.user
        view = WorkflowLevel2SortViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=workflowlevel2sort.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            WorkflowLevel2Sort.DoesNotExist,
            WorkflowLevel2Sort.objects.get, pk=workflowlevel2sort.pk)

    def test_delete_workflowlevel2sort_diff_org_normal_user(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        another_org = factories.Organization(name='Another Org')
        wflvl1 = factories.WorkflowLevel1(organization=another_org)
        workflowlevel2sort = factories.WorkflowLevel2Sort(workflowlevel1=wflvl1)

        request = self.factory.delete('/api/workflowlevel2sort/')
        request.user = self.tola_user.user
        view = WorkflowLevel2SortViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=workflowlevel2sort.pk)
        self.assertEquals(response.status_code, 403)
        WorkflowLevel2Sort.objects.get(pk=workflowlevel2sort.pk)
