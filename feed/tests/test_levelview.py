from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import json
import factories
from feed.views import LevelViewSet
from indicators.models import Level
from workflow.models import WorkflowTeam, ROLE_ORGANIZATION_ADMIN, \
    ROLE_PROGRAM_TEAM, ROLE_PROGRAM_ADMIN, ROLE_VIEW_ONLY


class LevelListViewsTest(TestCase):
    def setUp(self):
        factories.Level.create_batch(2)
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_list_level_superuser(self):
        request = self.factory.get('/api/level/')
        request.user = factories.User.build(is_superuser=True,
                                            is_staff=True)
        view = LevelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_level_org_admin(self):
        request = self.factory.get('/api/level/')
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.Level(organization=self.tola_user.organization)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_level_program_admin(self):
        request = self.factory.get('/api/level/')
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.Level(organization=self.tola_user.organization)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_level_program_team(self):
        request = self.factory.get('/api/level/')
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.Level(organization=self.tola_user.organization)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_level_normaluser(self):
        request = self.factory.get('/api/level/')
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.Level(organization=self.tola_user.organization)
        view = LevelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class LevelCreateViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        factories.Group()

    def test_create_level_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.post('/api/level/')
        wflvl1 = factories.WorkflowLevel1()
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': 'Goal',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/level/', data)
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Goal')

    def test_create_level_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.post('/api/level/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': 'Goal',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/level/', data)
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Goal')

    def test_create_level_program_admin(self):
        request = self.factory.post('/api/level/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        data = {'name': 'Goal',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/level/', data)
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Goal')

    def test_create_level_program_admin_json(self):
        request = self.factory.post('/api/level/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        data = {'name': 'Goal',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/level/', json.dumps(data),
                                    content_type='application/json')
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Goal')

    def test_create_level_program_team(self):
        request = self.factory.post('/api/level/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))

        data = {'name': 'Goal',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/level/', data)
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Goal')

    def test_create_level_view_only(self):
        request = self.factory.post('/api/level/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_VIEW_ONLY))

        data = {'name': 'Goal',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/level/', data)
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 403)


class LevelUpdateViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        factories.Group()

    def test_update_unexisting_level(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        data = {'name': 'Intermediate Results'}
        request = self.factory.post('/api/level/', data)
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'post': 'update'})
        response = view(request, pk=288)
        self.assertEqual(response.status_code, 404)

    def test_update_level_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        level = factories.Level()
        data = {'name': 'Goal'}
        request = self.factory.post('/api/level/', data)
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'post': 'update'})
        response = view(request, pk=level.pk)
        self.assertEqual(response.status_code, 200)

        level = Level.objects.get(pk=response.data['id'])
        self.assertEquals(level.name, data['name'])

    def test_update_level_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        level = factories.Level(organization=self.tola_user.organization)
        data = {'name': 'Goal'}
        request = self.factory.post('/api/level/', data)
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'post': 'update'})
        response = view(request, pk=level.pk)
        self.assertEqual(response.status_code, 200)

        level = Level.objects.get(pk=response.data['id'])
        self.assertEquals(level.name, data['name'])

    def test_update_level_diff_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        another_org = factories.Organization(name='Another Org')
        level = factories.Level(organization=another_org)
        data = {'name': 'Goal'}
        request = self.factory.post('/api/level/', data)
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'post': 'update'})
        response = view(request, pk=level.pk)
        self.assertEqual(response.status_code, 403)

    def test_update_level_program_admin(self):
        wflvl1 = factories.WorkflowLevel1()
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        level = factories.Level(organization=self.tola_user.organization,
                                workflowlevel1=wflvl1)

        data = {'name': 'Goal'}
        request = self.factory.post('/api/level/', data)
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'post': 'update'})
        response = view(request, pk=level.pk)
        self.assertEqual(response.status_code, 200)

        level = Level.objects.get(pk=response.data['id'])
        self.assertEquals(level.name, data['name'])

    def test_update_level_program_admin_json(self):
        wflvl1 = factories.WorkflowLevel1()
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        level = factories.Level(organization=self.tola_user.organization,
                                workflowlevel1=wflvl1)

        data = {'name': 'Goal'}
        request = self.factory.post('/api/level/', json.dumps(data),
                                    content_type='application/json')
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'post': 'update'})
        response = view(request, pk=level.pk)
        self.assertEqual(response.status_code, 200)

        level = Level.objects.get(pk=response.data['id'])
        self.assertEquals(level.name, data['name'])

    def test_update_level_program_team(self):
        wflvl1 = factories.WorkflowLevel1()
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))
        level = factories.Level(organization=self.tola_user.organization,
                                workflowlevel1=wflvl1)

        data = {'name': 'Goal'}
        request = self.factory.post('/api/level/', data)
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'post': 'update'})
        response = view(request, pk=level.pk)
        self.assertEqual(response.status_code, 200)

        level = Level.objects.get(pk=response.data['id'])
        self.assertEquals(level.name, data['name'])

    def test_update_level_view_only(self):
        wflvl1 = factories.WorkflowLevel1()
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_VIEW_ONLY))
        level = factories.Level(organization=self.tola_user.organization,
                                workflowlevel1=wflvl1)

        data = {'name': 'Goal'}
        request = self.factory.post('/api/level/', data)
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'post': 'update'})
        response = view(request, pk=level.pk)
        self.assertEqual(response.status_code, 403)


class LevelDeleteViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        factories.Group()

    def test_delete_level_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        level = factories.Level()
        request = self.factory.delete('/api/level/')
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=level.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Level.DoesNotExist,
            Level.objects.get, pk=level.pk)

    def test_delete_level_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        level = factories.Level(organization=self.tola_user.organization)
        request = self.factory.delete('/api/level/')
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=level.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Level.DoesNotExist,
            Level.objects.get, pk=level.pk)

    def test_delete_level_diff_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        another_org = factories.Organization(name='Another Org')
        level = factories.Level(organization=another_org)
        request = self.factory.delete('/api/level/')
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=level.pk)
        self.assertEquals(response.status_code, 403)
        Level.objects.get(pk=level.pk)

    def test_delete_level_program_admin(self):
        wflvl1 = factories.WorkflowLevel1()
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        level = factories.Level(organization=self.tola_user.organization,
                                workflowlevel1=wflvl1)

        request = self.factory.delete('/api/level/')
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=level.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Level.DoesNotExist,
            Level.objects.get, pk=level.pk)

    def test_delete_level_diff_org(self):
        wflvl1 = factories.WorkflowLevel1()
        another_org = factories.Organization(name='Another Org')
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        level = factories.Level(organization=another_org,
                                workflowlevel1=wflvl1)

        request = self.factory.delete('/api/level/')
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=level.pk)
        self.assertEquals(response.status_code, 403)
        Level.objects.get(pk=level.pk)

    def test_delete_level_program_team(self):
        wflvl1 = factories.WorkflowLevel1()
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))
        level = factories.Level(organization=self.tola_user.organization,
                                workflowlevel1=wflvl1)

        request = self.factory.delete('/api/level/')
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=level.pk)
        self.assertEquals(response.status_code, 403)
        Level.objects.get(pk=level.pk)

    def test_delete_level_view_only(self):
        wflvl1 = factories.WorkflowLevel1()
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_VIEW_ONLY))
        level = factories.Level(organization=self.tola_user.organization,
                                workflowlevel1=wflvl1)

        request = self.factory.delete('/api/level/')
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=level.pk)
        self.assertEquals(response.status_code, 403)
        Level.objects.get(pk=level.pk)

    def test_delete_level_normal_user(self):
        level = factories.Level()
        request = self.factory.delete('/api/level/')
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=level.pk)
        self.assertEquals(response.status_code, 403)
        Level.objects.get(pk=level.pk)

        
class LevelFilterViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_filter_level_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        another_org = factories.Organization(name='Another Org')
        level1 = factories.Level(
            name='Level 1',
            organization=self.tola_user.organization)
        factories.Level(name='Level 2', organization=another_org)

        request = self.factory.get(
            '/api/level/?organization__id=%s' %
            self.tola_user.organization.pk)
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], level1.name)

    def test_filter_level_normaluser(self):
        country1 = factories.Country(country='Brazil', code='BR')
        country2 = factories.Country()
        level1 = factories.Level(
            name='Level 1',
            country=country1,
            organization=self.tola_user.organization
        )
        factories.Level(name='Level 2', country=country2,
                        organization=self.tola_user.organization)

        request = self.factory.get(
            '/api/level/?country__country=%s' %
            country1.country)
        request.user = self.tola_user.user
        view = LevelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], level1.name)
