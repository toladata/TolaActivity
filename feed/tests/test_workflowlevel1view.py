from django.contrib.auth.models import User, Group
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from feed.views import WorkflowLevel1ViewSet, ROLE_PROGRAM_ADMIN
from workflow.models import Organization, TolaUser, WorkflowTeam, WorkflowLevel1


class WorkflowLevel1ViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.organization = Organization.objects.create(name="TestOrg")
        TolaUser.objects.create(user=self.user, organization=self.organization)
        Group.objects.create(name=ROLE_PROGRAM_ADMIN)

    def test_create_workflowlevel1(self):
        factory = APIRequestFactory()
        data = {'name': 'Save the Children'}
        self.request = factory.post('/api/workflowlevel1/', data)
        self.request.user = self.user
        view = WorkflowLevel1ViewSet.as_view({'post': 'create'})
        response = view(self.request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Save the Children')
        wft = WorkflowTeam.objects.get(workflowlevel1__id=response.data['id'])
        self.assertEqual(wft.workflow_user, self.user.tola_user)
        wflvl1 = WorkflowLevel1.objects.get(pk=response.data['id'])
        self.assertEqual(wflvl1.organization, self.organization)
        self.assertEqual(wflvl1.user_access.all().count(), 1)
        self.assertEqual(wflvl1.user_access.first(), self.user.tola_user)
