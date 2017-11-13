from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import WorkflowTeamViewSet
from workflow.models import WorkflowTeam


class WorkflowTeamViewsTest(TestCase):
    def setUp(self):
        factories.WorkflowTeam()

        factory = APIRequestFactory()
        self.request_get = factory.get('/api/workflowteam/')

    def test_list_workflowteam_superuser(self):
        self.request_get.user = factories.User.build(is_superuser=True, is_staff=True)
        view = WorkflowTeamViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_workflowteam_normaluser(self):
        tola_user = factories.TolaUser()
        self.request_get.user = tola_user.user
        view = WorkflowTeamViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_workflowteam_normaluser_one_result(self):
        tola_user = factories.TolaUser()
        wflvl1 = factories.WorkflowLevel1()
        WorkflowTeam.objects.create(workflowlevel1=wflvl1,
                                    workflow_user=tola_user)

        self.request_get.user = tola_user.user
        view = WorkflowTeamViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
