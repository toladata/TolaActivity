from django.contrib.auth.models import User
from django.test import TestCase
from django.test.utils import override_settings
from rest_framework.test import APIRequestFactory

from feed.views import ChecklistViewSet
from workflow.models import Checklist, Organization, TolaUser, WorkflowLevel1, WorkflowLevel2


class ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        wflvl1 = WorkflowLevel1.objects.create(name='WorkflowLevel1')
        wflvl2 = WorkflowLevel2.objects.create(name='WorkflowLevel2', workflowlevel1=wflvl1)
        Checklist.objects.bulk_create([
            Checklist(name='CheckList_0', workflowlevel2=wflvl2),
            Checklist(name='CheckList_1', workflowlevel2=wflvl2),
        ])

        factory = APIRequestFactory()
        self.request = factory.get('/api/checklist/')

    def test_list_checklist_superuser(self):
        self.request.user = self.user
        view = ChecklistViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_checklist_normaluser(self):
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save()
        organization = Organization.objects.create(name="TestOrg")
        TolaUser.objects.create(user=self.user, organization=organization)

        self.request.user = self.user
        view = ChecklistViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_checklist_normaluser_one_result(self):
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save()
        organization = Organization.objects.create(name="TestOrg")
        TolaUser.objects.create(user=self.user, organization=organization)

        wflvl1 = WorkflowLevel1.objects.create(name='WorkflowLevel1', organization=organization)
        wflvl2 = WorkflowLevel2.objects.create(name='WorkflowLevel2', workflowlevel1=wflvl1)
        Checklist.objects.create(name='CheckList_0', workflowlevel2=wflvl2)

        self.request.user = self.user
        view = ChecklistViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
