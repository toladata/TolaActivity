from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import factories
from feed.views import CollectedDataViewSet
from indicators.models import CollectedData
from workflow.models import WorkflowLevel1, WorkflowTeam, \
    ROLE_ORGANIZATION_ADMIN, ROLE_PROGRAM_TEAM, ROLE_PROGRAM_ADMIN, \
    ROLE_VIEW_ONLY


class CollectedDataListViewsTest(TestCase):
    def setUp(self):
        factories.CollectedData.create_batch(2)
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_list_collecteddata_superuser(self):
        request = self.factory.get('/api/collecteddata/')
        request.user = factories.User.build(is_superuser=True,
                                            is_staff=True)
        view = CollectedDataViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_collecteddata_org_admin(self):
        request = self.factory.get('/api/collecteddata/')
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1)
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        factories.CollectedData(workflowlevel1=wflvl1, indicator=indicator)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_collecteddata_program_admin(self):
        request = self.factory.get('/api/collecteddata/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        factories.CollectedData(workflowlevel1=wflvl1, indicator=indicator)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_collecteddata_program_team(self):
        request = self.factory.get('/api/collecteddata/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        factories.CollectedData(workflowlevel1=wflvl1, indicator=indicator)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_collecteddata_normaluser(self):
        request = self.factory.get('/api/collecteddata/')
        wflvl1 = factories.WorkflowLevel1()
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1)
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        factories.CollectedData(workflowlevel1=wflvl1, indicator=indicator)
        view = CollectedDataViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class CollectedDataCreateViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        factories.Group()

    def test_create_collecteddata_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.post('/api/collecteddata/')
        wflvl1 = factories.WorkflowLevel1()
        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        indicator_url = reverse('indicator-detail', kwargs={'pk': indicator.id},
                                request=request)

        data = {'indicator': indicator_url}

        request = self.factory.post('/api/collecteddata/', data)
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['indicator'], indicator_url)

    def test_create_collecteddata_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.post('/api/collecteddata/')
        wflvl1 = factories.WorkflowLevel1()
        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        indicator_url = reverse('indicator-detail', kwargs={'pk': indicator.id},
                                request=request)

        data = {'indicator': indicator_url}

        request = self.factory.post('/api/collecteddata/', data)
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['indicator'], indicator_url)

    def test_create_collecteddata_program_admin(self):
        request = self.factory.post('/api/collecteddata/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        indicator_url = reverse('indicator-detail', kwargs={'pk': indicator.id},
                                request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        data = {'indicator': indicator_url,
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/collecteddata/', data)
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['indicator'], indicator_url)

    def test_create_level_program_team(self):
        request = self.factory.post('/api/collecteddata/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        indicator_url = reverse('indicator-detail', kwargs={'pk': indicator.id},
                                request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))

        data = {'indicator': indicator_url,
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/collecteddata/', data)
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['indicator'], indicator_url)

    def test_create_level_view_only(self):
        request = self.factory.post('/api/collecteddata/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': wflvl1.id},
                             request=request)
        indicator_url = reverse('indicator-detail', kwargs={'pk': indicator.id},
                                request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_VIEW_ONLY))

        data = {'indicator': indicator_url,
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/collecteddata/', data)
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 403)


class CollectedDataUpdateViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        factories.Group()

    def test_update_unexisting_collecteddata(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        data = {'description': 'Intermediate Results'}
        request = self.factory.post('/api/collecteddata/', data)
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'post': 'update'})
        response = view(request, pk=288)
        self.assertEqual(response.status_code, 404)

    def test_update_collecteddata_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.post('/api/collecteddata/')
        collecteddata = factories.CollectedData()
        indicator_url = reverse('indicator-detail',
                                kwargs={'pk': collecteddata.indicator.id},
                                request=request)

        data = {'indicator': indicator_url,
                'description': 'Intermediate Results'}
        request = self.factory.post('/api/collecteddata/', data)
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'post': 'update'})
        response = view(request, pk=collecteddata.pk)
        self.assertEqual(response.status_code, 200)

        collecteddata = CollectedData.objects.get(pk=response.data['id'])
        self.assertEquals(collecteddata.description, data['description'])

    def test_update_collecteddata_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        collecteddata = factories.CollectedData(workflowlevel1=wflvl1)
        request = self.factory.post('/api/collecteddata/')
        indicator_url = reverse('indicator-detail',
                                kwargs={'pk': collecteddata.indicator.id},
                                request=request)

        data = {'indicator': indicator_url,
                'description': 'Intermediate Results'}
        request = self.factory.post('/api/collecteddata/', data)
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'post': 'update'})
        response = view(request, pk=collecteddata.pk)
        self.assertEqual(response.status_code, 200)

        collecteddata = CollectedData.objects.get(pk=response.data['id'])
        self.assertEquals(collecteddata.description, data['description'])

    def test_update_collecteddata_diff_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        another_org = factories.Organization(name='Another Org')
        wflvl1 = factories.WorkflowLevel1(organization=another_org)
        collecteddata = factories.CollectedData(workflowlevel1=wflvl1)
        request = self.factory.post('/api/collecteddata/')
        indicator_url = reverse('indicator-detail',
                                kwargs={'pk': collecteddata.indicator.id},
                                request=request)

        data = {'indicator': indicator_url,
                'description': 'Intermediate Results'}
        request = self.factory.post('/api/collecteddata/', data)
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'post': 'update'})
        response = view(request, pk=collecteddata.pk)
        self.assertEqual(response.status_code, 403)

    def test_update_collecteddata_program_admin(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        collecteddata = factories.CollectedData(workflowlevel1=wflvl1)
        request = self.factory.post('/api/collecteddata/')
        indicator_url = reverse('indicator-detail',
                                kwargs={'pk': collecteddata.indicator.id},
                                request=request)

        data = {'indicator': indicator_url,
                'description': 'Intermediate Results'}
        request = self.factory.post('/api/collecteddata/', data)
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'post': 'update'})
        response = view(request, pk=collecteddata.pk)
        self.assertEqual(response.status_code, 200)

        collecteddata = CollectedData.objects.get(pk=response.data['id'])
        self.assertEquals(collecteddata.description, data['description'])

    def test_update_collecteddata_program_team(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))
        collecteddata = factories.CollectedData(workflowlevel1=wflvl1)
        request = self.factory.post('/api/collecteddata/')
        indicator_url = reverse('indicator-detail',
                                kwargs={'pk': collecteddata.indicator.id},
                                request=request)

        data = {'indicator': indicator_url,
                'description': 'Intermediate Results'}
        request = self.factory.post('/api/collecteddata/', data)
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'post': 'update'})
        response = view(request, pk=collecteddata.pk)
        self.assertEqual(response.status_code, 200)

        collecteddata = CollectedData.objects.get(pk=response.data['id'])
        self.assertEquals(collecteddata.description, data['description'])

    def test_update_collecteddata_view_only(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_VIEW_ONLY))
        collecteddata = factories.CollectedData(workflowlevel1=wflvl1)
        request = self.factory.post('/api/collecteddata/')
        indicator_url = reverse('indicator-detail',
                                kwargs={'pk': collecteddata.indicator.id},
                                request=request)

        data = {'indicator': indicator_url,
                'description': 'Intermediate Results'}
        request = self.factory.post('/api/collecteddata/', data)
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'post': 'update'})
        response = view(request, pk=collecteddata.pk)
        self.assertEqual(response.status_code, 403)


class CollectedDataDeleteViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        factories.Group()

    def test_delete_collecteddata_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        collecteddata = factories.CollectedData()
        request = self.factory.delete('/api/collecteddata/')
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=collecteddata.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            CollectedData.DoesNotExist,
            CollectedData.objects.get, pk=collecteddata.pk)

    def test_delete_collecteddata_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        collecteddata = factories.CollectedData(workflowlevel1=wflvl1)
        request = self.factory.delete('/api/collecteddata/')
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=collecteddata.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            CollectedData.DoesNotExist,
            CollectedData.objects.get, pk=collecteddata.pk)

    def test_delete_collecteddata_diff_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        another_org = factories.Organization(name='Another Org')
        wflvl1 = factories.WorkflowLevel1(organization=another_org)
        collecteddata = factories.CollectedData(workflowlevel1=wflvl1)
        request = self.factory.delete('/api/collecteddata/')
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=collecteddata.pk)
        self.assertEquals(response.status_code, 403)
        CollectedData.objects.get(pk=collecteddata.pk)

    def test_delete_collecteddata_program_admin(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        collecteddata = factories.CollectedData(workflowlevel1=wflvl1)

        request = self.factory.delete('/api/collecteddata/')
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=collecteddata.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            CollectedData.DoesNotExist,
            CollectedData.objects.get, pk=collecteddata.pk)

    def test_delete_collecteddata_diff_org(self):
        another_org = factories.Organization(name='Another Org')
        wflvl1 = factories.WorkflowLevel1(organization=another_org)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        collecteddata = factories.CollectedData(workflowlevel1=wflvl1)

        request = self.factory.delete('/api/collecteddata/')
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=collecteddata.pk)
        self.assertEquals(response.status_code, 403)
        CollectedData.objects.get(pk=collecteddata.pk)

    def test_delete_collecteddata_program_team(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))
        collecteddata = factories.CollectedData(workflowlevel1=wflvl1)

        request = self.factory.delete('/api/collecteddata/')
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=collecteddata.pk)
        self.assertEquals(response.status_code, 403)
        CollectedData.objects.get(pk=collecteddata.pk)

    def test_delete_collecteddata_view_only(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_VIEW_ONLY))
        collecteddata = factories.CollectedData(workflowlevel1=wflvl1)

        request = self.factory.delete('/api/collecteddata/')
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=collecteddata.pk)
        self.assertEquals(response.status_code, 403)
        CollectedData.objects.get(pk=collecteddata.pk)

    def test_delete_collecteddata_normal_user(self):
        collecteddata = factories.CollectedData()
        request = self.factory.delete('/api/collecteddata/')
        request.user = self.tola_user.user
        view = CollectedDataViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=collecteddata.pk)
        self.assertEquals(response.status_code, 403)
        CollectedData.objects.get(pk=collecteddata.pk)
