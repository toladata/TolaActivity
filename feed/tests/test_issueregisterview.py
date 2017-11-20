from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import IssueRegisterViewSet


class IssueRegisterListViewTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()
        factories.IssueRegister.create_batch(2)
        self.factory = APIRequestFactory()

    def test_list_issueregister_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.get('/api/issueregister/')
        request.user = self.tola_user.user
        view = IssueRegisterViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_issueregister_normaluser(self):
        view = IssueRegisterViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/issueregister/')
        request.user = self.tola_user.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_issueregister_normaluser_one_result(self):
        factories.IssueRegister(
            name='IssueRegister0', organization=self.tola_user.organization)
        view = IssueRegisterViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/issueregister/')
        request.user = self.tola_user.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class IssueRegisterCreateViewTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()
        self.factory = APIRequestFactory()

    def test_create_issueregister_normaluser_one_result(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.post('/api/issueregister/')
        request.user = self.tola_user.user
        view = IssueRegisterViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)

        # check if the obj created has the user organization
        request = self.factory.get('/api/issueregister/')
        request.user = self.tola_user.user
        view = IssueRegisterViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class IssueRegisterFilterViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_filter_issueregister_org_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        another_org = factories.Organization(name='Another Org')
        wkflvl1_1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wkflvl1_2 = factories.WorkflowLevel1(organization=another_org)
        wkflvl2_1 = factories.WorkflowLevel2(workflowlevel1=wkflvl1_1)
        wkflvl2_2 = factories.WorkflowLevel2(workflowlevel1=wkflvl1_2)
        issueregister1 = factories.IssueRegister(workflowlevel2=wkflvl2_1)
        factories.IssueRegister(name='coded_field_b', workflowlevel2=wkflvl2_2)

        request = self.factory.get(
            '/api/issueregister'
            '/?workflowlevel2__workflowlevel1__organization__id=%s'
            % self.tola_user.organization.pk)
        request.user = self.tola_user.user
        view = IssueRegisterViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], issueregister1.name)
