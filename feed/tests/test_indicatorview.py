from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import json
import factories
from feed.views import IndicatorViewSet
from indicators.models import Indicator
from workflow.models import WorkflowLevel1, WorkflowTeam, \
    ROLE_ORGANIZATION_ADMIN, ROLE_PROGRAM_TEAM, ROLE_PROGRAM_ADMIN, \
    ROLE_VIEW_ONLY


class IndicatorListViewsTest(TestCase):
    def setUp(self):
        factories.Indicator.create_batch(2)
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_list_indicator_superuser(self):
        request = self.factory.get('/api/indicator/')
        request.user = factories.User.build(is_superuser=True,
                                            is_staff=True)
        view = IndicatorViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_indicator_org_admin(self):
        request = self.factory.get('/api/indicator/')
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1)
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.Indicator(workflowlevel1=[wflvl1])
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_indicator_program_admin(self):
        request = self.factory.get('/api/indicator/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.Indicator(workflowlevel1=[wflvl1])
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_indicator_program_team(self):
        request = self.factory.get('/api/indicator/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.Indicator(workflowlevel1=[wflvl1])
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_indicator_normaluser(self):
        request = self.factory.get('/api/indicator/')
        wflvl1 = factories.WorkflowLevel1()
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1)
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.Indicator(workflowlevel1=[wflvl1])
        view = IndicatorViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class IndicatorCreateViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        factories.Group()

    def test_create_indicator_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.post('/api/indicator/')
        wflvl1 = factories.WorkflowLevel1()
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': 'Building resilience in Mali',
                'workflowlevel1': [wflvl1_url]}

        request = self.factory.post('/api/indicator/', data)
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Building resilience in Mali')

    def test_create_indicator_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.post('/api/indicator/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': 'Building resilience in Mali',
                'workflowlevel1': [wflvl1_url]}

        request = self.factory.post('/api/indicator/', data)
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Building resilience in Mali')

    def test_create_indicator_program_admin(self):
        request = self.factory.post('/api/indicator/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        wflvl2 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl2_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl2.id},
                             request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        data = {'name': 'Building resilience in Mali',
                'workflowlevel1': [wflvl1_url, wflvl2_url]}

        request = self.factory.post('/api/indicator/', data)
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Building resilience in Mali')

    def test_create_indicator_program_admin_json(self):
        request = self.factory.post('/api/indicator/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)

        wflvl2 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl2_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl2.id},
                             request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        data = {'name': 'Building resilience in Mali',
                'workflowlevel1': [wflvl1_url, wflvl2_url]}
        request = self.factory.post('/api/indicator/', json.dumps(data),
                                    content_type='application/json')
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Building resilience in Mali')

    def test_create_level_program_team(self):
        request = self.factory.post('/api/indicator/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))

        data = {'name': 'Building resilience in Mali',
                'workflowlevel1': [wflvl1_url]}

        request = self.factory.post('/api/indicator/', data)
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Building resilience in Mali')

    def test_create_level_view_only(self):
        request = self.factory.post('/api/indicator/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_VIEW_ONLY))

        data = {'name': 'Building resilience in Mali',
                'workflowlevel1': [wflvl1_url]}

        request = self.factory.post('/api/indicator/', data)
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 403)


class IndicatorUpdateViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        factories.Group()

    def test_update_unexisting_indicator(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        data = {'name': 'Number of beneficiaries registered'}
        request = self.factory.post('/api/indicator/', data)
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'post': 'update'})
        response = view(request, pk=288)
        self.assertEqual(response.status_code, 404)

    def test_update_indicator_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.post('/api/indicator/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        wflvl1_url = reverse('workflowlevel1-detail', kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': 'Number of beneficiaries registered',
                'workflowlevel1': wflvl1_url}
        request = self.factory.post('/api/indicator/', data)
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'post': 'update'})
        response = view(request, pk=indicator.pk)
        self.assertEqual(response.status_code, 200)

        indicator = Indicator.objects.get(pk=response.data['id'])
        self.assertEquals(indicator.name, data['name'])

    def test_update_indicator_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.post('/api/indicator/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        wflvl1_url = reverse('workflowlevel1-detail', kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': 'Number of beneficiaries registered',
                'workflowlevel1': wflvl1_url}
        request = self.factory.post('/api/indicator/', data)
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'post': 'update'})
        response = view(request, pk=indicator.pk)
        self.assertEqual(response.status_code, 200)

        indicator = Indicator.objects.get(pk=response.data['id'])
        self.assertEquals(indicator.name, data['name'])

    def test_update_indicator_program_admin(self):
        request = self.factory.post('/api/indicator/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        wflvl1_url = reverse('workflowlevel1-detail', kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': 'Number of beneficiaries registered',
                'workflowlevel1': wflvl1_url}
        request = self.factory.post('/api/indicator/', data)
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'post': 'update'})
        response = view(request, pk=indicator.pk)
        self.assertEqual(response.status_code, 200)

        indicator = Indicator.objects.get(pk=response.data['id'])
        self.assertEquals(indicator.name, data['name'])

    def test_update_indicator_program_team(self):
        request = self.factory.post('/api/indicator/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))
        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        wflvl1_url = reverse('workflowlevel1-detail', kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': 'Number of beneficiaries registered',
                'workflowlevel1': wflvl1_url}
        request = self.factory.post('/api/indicator/', data)
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'post': 'update'})
        response = view(request, pk=indicator.pk)
        self.assertEqual(response.status_code, 200)

        indicator = Indicator.objects.get(pk=response.data['id'])
        self.assertEquals(indicator.name, data['name'])

    def test_update_indicator_view_only(self):
        request = self.factory.post('/api/indicator/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_VIEW_ONLY))
        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        wflvl1_url = reverse('workflowlevel1-detail', kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': 'Number of beneficiaries registered',
                'workflowlevel1': wflvl1_url}
        request = self.factory.post('/api/indicator/', data)
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'post': 'update'})
        response = view(request, pk=indicator.pk)
        self.assertEqual(response.status_code, 403)


class IndicatorDeleteViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        factories.Group()

    def test_delete_indicator_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        wflvl1 = factories.WorkflowLevel1()
        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        request = self.factory.delete('/api/indicator/')
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=indicator.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Indicator.DoesNotExist,
            Indicator.objects.get, pk=indicator.pk)

    def test_delete_indicator_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        request = self.factory.delete('/api/indicator/')
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=indicator.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Indicator.DoesNotExist,
            Indicator.objects.get, pk=indicator.pk)

    def test_delete_indicator_diff_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        another_org = factories.Organization(name='Another Org')
        wflvl1 = factories.WorkflowLevel1(organization=another_org)
        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        request = self.factory.delete('/api/indicator/')
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=indicator.pk)
        self.assertEquals(response.status_code, 403)
        Indicator.objects.get(pk=indicator.pk)

    def test_delete_indicator_program_admin(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        indicator = factories.Indicator(workflowlevel1=[wflvl1])

        request = self.factory.delete('/api/indicator/')
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=indicator.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Indicator.DoesNotExist,
            Indicator.objects.get, pk=indicator.pk)

    def test_delete_indicator_diff_org(self):
        another_org = factories.Organization(name='Another Org')
        wflvl1 = factories.WorkflowLevel1(organization=another_org)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        indicator = factories.Indicator(workflowlevel1=[wflvl1])

        request = self.factory.delete('/api/indicator/')
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=indicator.pk)
        self.assertEquals(response.status_code, 403)
        Indicator.objects.get(pk=indicator.pk)

    def test_delete_indicator_program_team(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))
        indicator = factories.Indicator(workflowlevel1=[wflvl1])

        request = self.factory.delete('/api/indicator/')
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=indicator.pk)
        self.assertEquals(response.status_code, 403)
        Indicator.objects.get(pk=indicator.pk)

    def test_delete_indicator_view_only(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_VIEW_ONLY))
        indicator = factories.Indicator(workflowlevel1=[wflvl1])

        request = self.factory.delete('/api/indicator/')
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=indicator.pk)
        self.assertEquals(response.status_code, 403)
        Indicator.objects.get(pk=indicator.pk)

    def test_delete_indicator_normal_user(self):
        indicator = factories.Indicator()
        request = self.factory.delete('/api/indicator/')
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=indicator.pk)
        self.assertEquals(response.status_code, 403)
        Indicator.objects.get(pk=indicator.pk)
