from django.contrib.auth.models import Group
from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import WorkflowLevel1ViewSet, ROLE_PROGRAM_ADMIN
from workflow.models import WorkflowTeam, WorkflowLevel1


class WorkflowLevel1ViewsTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()
        factories.Group()

    def test_create_workflowlevel1(self):
        factory = APIRequestFactory()
        data = {'name': 'Save the Children'}
        self.request = factory.post('/api/workflowlevel1/', data)
        self.request.user = self.tola_user.user
        view = WorkflowLevel1ViewSet.as_view({'post': 'create'})
        response = view(self.request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Save the Children')
        wft = WorkflowTeam.objects.get(workflowlevel1__id=response.data['id'])
        self.assertEqual(wft.workflow_user, self.tola_user)
        wflvl1 = WorkflowLevel1.objects.get(pk=response.data['id'])
        self.assertEqual(wflvl1.organization, self.tola_user.organization)
        self.assertEqual(wflvl1.user_access.all().count(), 1)
        self.assertEqual(wflvl1.user_access.first(), self.tola_user)
