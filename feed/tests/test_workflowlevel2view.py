import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import factories
from feed.views import WorkflowLevel2ViewSet
from workflow.models import WorkflowLevel2, WorkflowTeam, ROLE_VIEW_ONLY, \
    ROLE_ORGANIZATION_ADMIN, ROLE_PROGRAM_ADMIN, ROLE_PROGRAM_TEAM


class WorkflowLevel2ListViewsTest(TestCase):
    def setUp(self):
        factories.WorkflowLevel2.create_batch(2)
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_list_workflowlevel2_superuser(self):
        request = self.factory.get('/api/workflowlevel2/')
        request.user = factories.User.build(is_superuser=True,
                                            is_staff=True)
        view = WorkflowLevel2ViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_workflowlevel2_org_admin(self):
        request = self.factory.get('/api/workflowlevel2/')
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        wflvl1 = factories.WorkflowLevel1()
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1)
        factories.WorkflowLevel2(workflowlevel1=wflvl1)
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        wflvl1.organization = self.tola_user.organization
        wflvl1.save()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_workflowlevel2_program_admin(self):
        request = self.factory.get('/api/workflowlevel2/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.WorkflowLevel2(workflowlevel1=wflvl1)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_workflowlevel2_program_team(self):
        request = self.factory.get('/api/workflowlevel2/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.WorkflowLevel2(workflowlevel1=wflvl1)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_workflowlevel2_view_only(self):
        request = self.factory.get('/api/workflowlevel2/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_VIEW_ONLY))
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.WorkflowLevel2(workflowlevel1=wflvl1)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class WorkflowLevel2CreateViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        factories.Group()

    def test_create_workflowlevel2_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.post('/api/workflowlevel2/')
        wflvl1 = factories.WorkflowLevel1()
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': 'Help Syrians',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/workflowlevel2/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Help Syrians')

    def test_create_workflowlevel2_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.post('/api/workflowlevel2/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': 'Help Syrians',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/workflowlevel2/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Help Syrians')

    def test_create_workflowlevel2_program_admin(self):
        request = self.factory.post('/api/workflowlevel2/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        tolauser_url = reverse('tolauser-detail',
                               kwargs={'pk': self.tola_user.id},
                               request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        data = {'name': 'Help Syrians',
                'workflowlevel1': wflvl1_url,
                'staff_responsible': tolauser_url}

        request = self.factory.post('/api/workflowlevel2/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Help Syrians')
        self.assertEqual(response.data['staff_responsible'], tolauser_url)

    def test_create_workflowlevel2_program_admin_json(self):
        request = self.factory.post('/api/workflowlevel2/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        data = {'name': 'Help Syrians',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/workflowlevel2/', json.dumps(data),
                                    content_type='application/json')
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Help Syrians')

    def test_create_workflowlevel2_program_team(self):
        request = self.factory.post('/api/workflowlevel2/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))

        data = {'name': 'Help Syrians',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/workflowlevel2/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Help Syrians')

    def test_create_workflowlevel2_view_only(self):
        request = self.factory.post('/api/workflowlevel2/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_VIEW_ONLY))

        data = {'name': 'Help Syrians',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/workflowlevel2/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 403)


class WorkflowLevel2UpdateViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        factories.Group()

    def test_update_unexisting_workflowlevel2(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        data = {'name': 'Community awareness program conducted to plant trees'}

        request = self.factory.post('/api/workflowlevel2/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'post': 'update'})
        response = view(request, pk=288)
        self.assertEqual(response.status_code, 404)

    def test_update_workflowlevel2_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.post('/api/workflowlevel2/')
        wflvl1 = factories.WorkflowLevel1()
        workflowlevel2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': 'Community awareness program conducted to plant trees',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/workflowlevel2/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'post': 'update'})
        response = view(request, pk=workflowlevel2.pk)
        self.assertEqual(response.status_code, 200)

        workflowlevel2 = WorkflowLevel2.objects.get(pk=response.data['id'])
        self.assertEquals(workflowlevel2.name, data['name'])

    def test_update_workflowlevel2_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.post('/api/workflowlevel2/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        workflowlevel2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': 'Community awareness program conducted to plant trees',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/workflowlevel2/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'post': 'update'})
        response = view(request, pk=workflowlevel2.pk)
        self.assertEqual(response.status_code, 200)

        workflowlevel2 = WorkflowLevel2.objects.get(pk=response.data['id'])
        self.assertEquals(workflowlevel2.name, data['name'])

    def test_update_workflowlevel2_diff_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.post('/api/workflowlevel2/')
        another_org = factories.Organization(name='Another Org')
        wflvl1 = factories.WorkflowLevel1(organization=another_org)
        workflowlevel2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': 'Community awareness program conducted to plant trees',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/workflowlevel2/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'post': 'update'})
        response = view(request, pk=workflowlevel2.pk)
        self.assertEqual(response.status_code, 403)

    def test_update_workflowlevel2_program_admin(self):
        request = self.factory.post('/api/workflowlevel2/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        workflowlevel2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': 'Community awareness program conducted to plant trees',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/workflowlevel2/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'post': 'update'})
        response = view(request, pk=workflowlevel2.pk)
        self.assertEqual(response.status_code, 200)

        workflowlevel2 = WorkflowLevel2.objects.get(pk=response.data['id'])
        self.assertEquals(workflowlevel2.name, data['name'])

    def test_update_workflowlevel2_program_admin_json(self):
        request = self.factory.post('/api/workflowlevel2/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        workflowlevel2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': 'Community awareness program conducted to plant trees',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/indicator/', json.dumps(data),
                                    content_type='application/json')
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'post': 'update'})
        response = view(request, pk=workflowlevel2.pk)
        self.assertEqual(response.status_code, 200)

        workflowlevel2 = WorkflowLevel2.objects.get(pk=response.data['id'])
        self.assertEquals(workflowlevel2.name, data['name'])

    def test_update_workflowlevel2_program_team(self):
        request = self.factory.post('/api/workflowlevel2/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))
        workflowlevel2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': 'Community awareness program conducted to plant trees',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/workflowlevel2/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'post': 'update'})
        response = view(request, pk=workflowlevel2.pk)
        self.assertEqual(response.status_code, 200)

        workflowlevel2 = WorkflowLevel2.objects.get(pk=response.data['id'])
        self.assertEquals(workflowlevel2.name, data['name'])

    def test_update_workflowlevel2_view_only(self):
        request = self.factory.post('/api/workflowlevel2/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_VIEW_ONLY))
        workflowlevel2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': 'Community awareness program conducted to plant trees',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/workflowlevel2/', data)
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'post': 'update'})
        response = view(request, pk=workflowlevel2.pk)
        self.assertEqual(response.status_code, 403)


class WorkflowLevel2DeleteViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        factories.Group()

    def test_delete_workflowlevel2_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        workflowlevel2 = factories.WorkflowLevel2()
        request = self.factory.delete('/api/workflowlevel2/')
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=workflowlevel2.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            WorkflowLevel2.DoesNotExist,
            WorkflowLevel2.objects.get, pk=workflowlevel2.pk)

    def test_delete_workflowlevel2_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        workflowlevel2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)

        request = self.factory.delete('/api/workflowlevel2/')
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=workflowlevel2.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            WorkflowLevel2.DoesNotExist,
            WorkflowLevel2.objects.get, pk=workflowlevel2.pk)

    def test_delete_workflowlevel2_diff_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        another_org = factories.Organization(name='Another Org')
        wflvl1 = factories.WorkflowLevel1(organization=another_org)
        workflowlevel2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)

        request = self.factory.delete('/api/workflowlevel2/')
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=workflowlevel2.pk)
        self.assertEquals(response.status_code, 403)
        WorkflowLevel2.objects.get(pk=workflowlevel2.pk)

    def test_delete_workflowlevel2_program_admin(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        workflowlevel2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)

        request = self.factory.delete('/api/workflowlevel2/')
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=workflowlevel2.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            WorkflowLevel2.DoesNotExist,
            WorkflowLevel2.objects.get, pk=workflowlevel2.pk)

    def test_delete_workflowlevel2_diff_org(self):
        another_org = factories.Organization(name='Another Org')
        wflvl1 = factories.WorkflowLevel1(organization=another_org)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        workflowlevel2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)

        request = self.factory.delete('/api/workflowlevel2/')
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=workflowlevel2.pk)
        self.assertEquals(response.status_code, 403)
        WorkflowLevel2.objects.get(pk=workflowlevel2.pk)

    def test_delete_workflowlevel2_program_team(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))
        workflowlevel2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)

        request = self.factory.delete('/api/workflowlevel2/')
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=workflowlevel2.pk)
        self.assertEquals(response.status_code, 403)
        WorkflowLevel2.objects.get(pk=workflowlevel2.pk)

    def test_delete_workflowlevel2_view_only(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_VIEW_ONLY))
        workflowlevel2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)

        request = self.factory.delete('/api/workflowlevel2/')
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=workflowlevel2.pk)
        self.assertEquals(response.status_code, 403)
        WorkflowLevel2.objects.get(pk=workflowlevel2.pk)

    def test_delete_workflowlevel2_normal_user(self):
        workflowlevel2 = factories.WorkflowLevel2()
        request = self.factory.delete('/api/workflowlevel2/')
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=workflowlevel2.pk)
        self.assertEquals(response.status_code, 403)
        WorkflowLevel2.objects.get(pk=workflowlevel2.pk)


class WorkflowLevel2FilterViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_filter_workflowlevel2_wkflvl1_country_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        country1 = factories.Country(country='Brazil', code='BR')
        country2 = factories.Country(country='Germany', code='DE')
        wkflvl1_1 = factories.WorkflowLevel1(country=[country1])
        wkflvl1_2 = factories.WorkflowLevel1(country=[country2])
        wkflvl2 = factories.WorkflowLevel2(workflowlevel1=wkflvl1_1)
        factories.WorkflowLevel2(
            name='Develop brief survey', workflowlevel1=wkflvl1_2)

        request = self.factory.get(
            '/api/workflowlevel2/?workflowlevel1__country__country=%s'
            % country1.country)
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], wkflvl2.name)

    def test_filter_workflowlevel2_wkflvl1_name_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        wkflvl1_1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wkflvl1_2 = factories.WorkflowLevel1(
            name='Construction Project',
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wkflvl1_1)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wkflvl1_2)
        wkflvl2 = factories.WorkflowLevel2(workflowlevel1=wkflvl1_1)
        factories.WorkflowLevel2(
            name='Develop brief survey', workflowlevel1=wkflvl1_2)

        request = self.factory.get(
            '/api/workflowlevel2/?workflowlevel1__name=%s'
            % wkflvl1_1.name)
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], wkflvl2.name)

    def test_filter_workflowlevel2_wkflvl1_id_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        wkflvl1_1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wkflvl1_2 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wkflvl1_1)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wkflvl1_2)
        wkflvl2 = factories.WorkflowLevel2(workflowlevel1=wkflvl1_1)
        factories.WorkflowLevel2(
            name='Develop brief survey', workflowlevel1=wkflvl1_2)

        request = self.factory.get(
            '/api/workflowlevel2/?workflowlevel1__id=%s'
            % wkflvl1_1.pk)
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], wkflvl2.name)

    def test_filter_workflowlevel2_level2_uuid_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        wkflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wkflvl1)
        wkflvl2 = factories.WorkflowLevel2(
            level2_uuid=111, workflowlevel1=wkflvl1)
        factories.WorkflowLevel2(
            name='Develop brief survey', level2_uuid=222,
            workflowlevel1=wkflvl1)

        request = self.factory.get(
            '/api/workflowlevel2/?level2_uuid=%s'
            % wkflvl2.level2_uuid)
        request.user = self.tola_user.user
        view = WorkflowLevel2ViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], wkflvl2.name)
