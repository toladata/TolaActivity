from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import CodedFieldViewSet


class CodedFieldListViewTest(TestCase):
    def setUp(self):
        factories.Organization(id=1)
        wflvl1 = factories.WorkflowLevel1()
        wflvl2 = factories.WorkflowLevel2(name='WorkflowLevel2',
                                          workflowlevel1=wflvl1)
        factories.CodedField.create_batch(2, workflowlevel2=[wflvl2])

        factory = APIRequestFactory()
        self.request = factory.get('/api/codedfield/')

    def test_list_codedfield_superuser(self):
        self.request.user = factories.User.build(is_superuser=True,
                                                 is_staff=True)
        view = CodedFieldViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_codedfield_normaluser(self):
        tola_user = factories.TolaUser()
        self.request.user = tola_user.user
        view = CodedFieldViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_codedfield_normaluser_one_result(self):
        tola_user = factories.TolaUser()
        factories.CodedField(organization=tola_user.organization)

        self.request.user = tola_user.user
        view = CodedFieldViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class CodedFieldCreateViewTest(TestCase):
    def setUp(self):
        self.user = factories.User(is_superuser=True, is_staff=True)
        factory = APIRequestFactory()
        self.request = factory.post('/api/codedfield/')

    def test_create_codedfield(self):
        factories.Organization(id=1)
        self.request.user = self.user
        view = CodedFieldViewSet.as_view({'post': 'create'})
        response = view(self.request)

        self.assertEqual(response.status_code, 201)


class CodedFieldFilterViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_filter_codedfield_org_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        another_org = factories.Organization(name='Another Org')
        wkflvl1_1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wkflvl1_2 = factories.WorkflowLevel1(organization=another_org)
        wkflvl2_1 = factories.WorkflowLevel2(workflowlevel1=wkflvl1_1)
        wkflvl2_2 = factories.WorkflowLevel2(workflowlevel1=wkflvl1_2)
        codedfield1 = factories.CodedField(workflowlevel2=[wkflvl2_1])
        factories.CodedField(name='coded_field_b', workflowlevel2=[wkflvl2_2])

        request = self.factory.get(
            '/api/codedfield/?workflowlevel2__workflowlevel1__organization__id'
            '=%s' % self.tola_user.organization.pk)
        request.user = self.tola_user.user
        view = CodedFieldViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], codedfield1.name)
