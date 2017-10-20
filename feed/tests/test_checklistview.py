from django.test import TestCase
from django.test.utils import override_settings
from rest_framework.test import APIRequestFactory

import factories
from feed.views import ChecklistViewSet
from workflow.models import Checklist, TolaUser, WorkflowLevel1, WorkflowLevel2


class ChecklistViewsTest(TestCase):
    def setUp(self):
        wflvl1 = WorkflowLevel1.objects.create(name='WorkflowLevel1')
        wflvl2 = WorkflowLevel2.objects.create(name='WorkflowLevel2', workflowlevel1=wflvl1)
        Checklist.objects.bulk_create([
            Checklist(name='CheckList_0', workflowlevel2=wflvl2),
            Checklist(name='CheckList_1', workflowlevel2=wflvl2),
        ])

        factory = APIRequestFactory()
        self.request = factory.get('/api/checklist/')

    def test_list_checklist_superuser(self):
        self.request.user = factories.User.build(is_superuser=True, is_staff=True)
        view = ChecklistViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_checklist_normaluser(self):
        user = factories.User()
        organization = factories.Organization()
        TolaUser.objects.create(user=user, organization=organization)

        self.request.user = user
        view = ChecklistViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_checklist_normaluser_one_result(self):
        user = factories.User()
        organization = factories.Organization()
        TolaUser.objects.create(user=user, organization=organization)

        wflvl1 = WorkflowLevel1.objects.create(name='WorkflowLevel1', organization=organization)
        wflvl2 = WorkflowLevel2.objects.create(name='WorkflowLevel2', workflowlevel1=wflvl1)
        Checklist.objects.create(name='CheckList_0', workflowlevel2=wflvl2)

        self.request.user = user
        view = ChecklistViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
