import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import factories
from feed.views import StakeholderViewSet
from workflow.models import Stakeholder, WorkflowLevel1, WorkflowTeam


class StakeholderListViewTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()
        factories.Stakeholder.create_batch(2)
        self.factory = APIRequestFactory()

    def test_list_stakeholder_superuser(self):
        self.tola_user.user.is_superuser = True
        self.tola_user.user.is_staff = True
        self.tola_user.user.save()

        request = self.factory.get('/api/stakeholder/')
        request.user = self.tola_user.user
        view = StakeholderViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_stakeholder_normaluser(self):
        request = self.factory.get('/api/stakeholder/')
        request.user = self.tola_user.user
        view = StakeholderViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_stakeholder_normaluser_one_result(self):
        wflvl1_1 = WorkflowLevel1.objects.create(name='WorkflowLevel1_1')
        wflvl1_2 = WorkflowLevel1.objects.create(name='WorkflowLevel1_2')
        WorkflowTeam.objects.create(workflow_user=self.tola_user,
                                    workflowlevel1=wflvl1_1)
        WorkflowTeam.objects.create(workflow_user=self.tola_user,
                                    workflowlevel1=wflvl1_2)
        stk = Stakeholder.objects.create(
            name='Stakeholder_0', organization=self.tola_user.organization)
        stk.workflowlevel1.add(wflvl1_1, wflvl1_2)

        request = self.factory.get('/api/stakeholder/')
        request.user = self.tola_user.user
        view = StakeholderViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class StakeholderCreateViewTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()
        self.factory = APIRequestFactory()
        Stakeholder.objects.create(name='Stakeholder_0',
                                   organization=self.tola_user.organization)

    def test_create_stakeholder_normaluser_one_result(self):
        request = self.factory.post('/api/stakeholder/')
        wflvl1 = WorkflowLevel1.objects.create(name='WorkflowLevel1')
        WorkflowTeam.objects.create(workflow_user=self.tola_user,
                                    workflowlevel1=wflvl1)
        user_url = reverse('user-detail', kwargs={'pk': self.tola_user.user.id},
                           request=request)

        # create stakeholder via POST request
        data = {'workflowlevel1': [
            'http://testserver/api/workflowlevel1/%s/' % wflvl1.id]}
        request = self.factory.post('/api/stakeholder/', data)
        request.user = self.tola_user.user
        view = StakeholderViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['created_by'], user_url)

        # check if the obj created has the user organization
        request = self.factory.get('/api/stakeholder/')
        request.user = self.tola_user.user
        view = StakeholderViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_stakeholder_normaluser_one_result_json(self):
        request = self.factory.post('/api/stakeholder/')
        wflvl1 = WorkflowLevel1.objects.create(name='WorkflowLevel1')
        WorkflowTeam.objects.create(workflow_user=self.tola_user,
                                    workflowlevel1=wflvl1)
        user_url = reverse('user-detail', kwargs={'pk': self.tola_user.user.id},
                           request=request)

        # create stakeholder via POST request
        data = {'workflowlevel1': [
            'http://testserver/api/workflowlevel1/%s/' % wflvl1.id]}
        request = self.factory.post(
            '/api/stakeholder/', json.dumps(data),
            content_type='application/json')
        request.user = self.tola_user.user
        view = StakeholderViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['created_by'], user_url)

        # check if the obj created has the user organization
        request = self.factory.get('/api/stakeholder/')
        request.user = self.tola_user.user
        view = StakeholderViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class StakeholderFilterViewTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()
        factories.Stakeholder.create_batch(2)
        self.factory = APIRequestFactory()

    def test_filter_stakeholder(self):
        wflvl1_1 = factories.WorkflowLevel1(name='WorkflowLevel1')
        wflvl1_2 = factories.WorkflowLevel1()
        factories.WorkflowTeam(workflow_user=self.tola_user,
                               workflowlevel1=wflvl1_1)
        factories.WorkflowTeam(workflow_user=self.tola_user,
                               workflowlevel1=wflvl1_2)
        stk1 = factories.Stakeholder(
            name='Stakeholder_1',
            organization=self.tola_user.organization,
            workflowlevel1=[wflvl1_1]
        )
        factories.Stakeholder(
            name='Stakeholder_2',
            organization=self.tola_user.organization,
            workflowlevel1=[wflvl1_2]
        )

        request = self.factory.get(
            '/api/stakeholder/?workflowlevel1__name=%s' % wflvl1_1.name)
        request.user = self.tola_user.user
        view = StakeholderViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], stk1.name)
