from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import StakeholderViewSet
from workflow.models import Stakeholder, Organization, WorkflowLevel1, \
    WorkflowTeam


class StakeholderViewsTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()
        Stakeholder.objects.create(name='Stakeholder_0',
                                   organization=self.tola_user.organization)

        factory = APIRequestFactory()
        self.request_get = factory.get('/api/stakeholder/')
        self.request_post = factory.post('/api/stakeholder/')

    def test_list_stakeholder_superuser(self):
        self.tola_user.user.is_superuser = True
        self.tola_user.user.is_staff = True
        self.tola_user.user.save()

        self.request_get.user = self.tola_user.user
        view = StakeholderViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_stakeholder_normaluser(self):
        self.request_get.user = self.tola_user.user
        view = StakeholderViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_stakeholder_normaluser_one_result(self):
        wflvl1 = WorkflowLevel1.objects.create(name='WorkflowLevel1')
        WorkflowTeam.objects.create(workflow_user=self.tola_user,
                                    workflowlevel1=wflvl1)
        stk = Stakeholder.objects.create(
            name='Stakeholder_0', organization=self.tola_user.organization)
        stk.workflowlevel1.add(wflvl1)

        self.request_get.user = self.tola_user.user
        view = StakeholderViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_stakeholder_normaluser_one_result(self):
        wflvl1 = WorkflowLevel1.objects.create(name='WorkflowLevel1')
        WorkflowTeam.objects.create(workflow_user=self.tola_user,
                                    workflowlevel1=wflvl1)

        # create stakeholder via POST request
        data = {'workflowlevel1': [
            'http://testserver/api/workflowlevel1/%s/' % wflvl1.id]}
        self.request_post = APIRequestFactory().post('/api/stakeholder/', data)
        self.request_post.user = self.tola_user.user
        view = StakeholderViewSet.as_view({'post': 'create'})
        response = view(self.request_post)
        self.assertEqual(response.status_code, 201)

        # check if the obj created has the user organization
        self.request_get.user = self.tola_user.user
        view = StakeholderViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
