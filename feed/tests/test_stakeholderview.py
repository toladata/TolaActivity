from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from feed.views import StakeholderViewSet
from workflow.models import Stakeholder, Organization, TolaUser, \
    WorkflowLevel1, WorkflowTeam


class StakeholderViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com',
                                             'johnpassword')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        organization = Organization.objects.create(name="TestOrg_0")
        Stakeholder.objects.create(name='Stakeholder_0',
                                   organization=organization)

        factory = APIRequestFactory()
        self.request_get = factory.get('/api/stakeholder/')
        self.request_post = factory.post('/api/stakeholder/')

    def test_list_stakeholder_superuser(self):
        self.request_get.user = self.user
        view = StakeholderViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_stakeholder_normaluser(self):
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save()
        organization = Organization.objects.create(name="TestOrg")
        TolaUser.objects.create(user=self.user, organization=organization)

        self.request_get.user = self.user
        view = StakeholderViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_stakeholder_normaluser_one_result(self):
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save()
        organization = Organization.objects.create(name="TestOrg_1")
        tola_user = TolaUser.objects.create(user=self.user,
                                            organization=organization)
        wflvl1 = WorkflowLevel1.objects.create(name='WorkflowLevel1')
        WorkflowTeam.objects.create(workflow_user=tola_user,
                                    workflowlevel1=wflvl1)
        stk = Stakeholder.objects.create(name='Stakeholder_0',
                                         organization=organization)
        stk.workflowlevel1.add(wflvl1)

        self.request_get.user = self.user
        view = StakeholderViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_stakeholder_normaluser_one_result(self):
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save()
        organization = Organization.objects.create(name="TestOrg_1")
        tola_user = TolaUser.objects.create(user=self.user,
                                            organization=organization)
        wflvl1 = WorkflowLevel1.objects.create(name='WorkflowLevel1')
        WorkflowTeam.objects.create(workflow_user=tola_user,
                                    workflowlevel1=wflvl1)

        # create stakeholder via POST request
        data = {'workflowlevel1': [
            'http://testserver/api/workflowlevel1/%s/' % wflvl1.id]}
        self.request_post = APIRequestFactory().post('/api/stakeholder/', data)
        self.request_post.user = self.user
        view = StakeholderViewSet.as_view({'post': 'create'})
        response = view(self.request_post)
        self.assertEqual(response.status_code, 201)

        # check if the obj created has the user organization
        self.request_get.user = self.user
        view = StakeholderViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
