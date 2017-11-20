from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

from feed.views import DocumentationViewSet
import factories
import json
from workflow.models import Documentation, WorkflowLevel1, WorkflowTeam, \
    ROLE_ORGANIZATION_ADMIN, ROLE_PROGRAM_TEAM, ROLE_PROGRAM_ADMIN, \
    ROLE_VIEW_ONLY


class DocumentationListViewTest(TestCase):
    def setUp(self):
        factories.Documentation.create_batch(2)
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_list_documentation_superuser(self):
        request = self.factory.get('/api/documentation/')
        request.user = factories.User.build(is_superuser=True,
                                            is_staff=True)
        view = DocumentationViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_documentation_normaluser(self):
        request = self.factory.get('/api/documentation/')
        request.user = self.tola_user.user
        view = DocumentationViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_documentation_normaluser_one_result(self):
        request = self.factory.get('/api/documentation/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl2 = factories.WorkflowLevel2(workflowlevel1=wflvl1)
        WorkflowTeam.objects.create(workflow_user=self.tola_user,
                                    workflowlevel1=wflvl1)
        factories.Documentation(workflowlevel1=wflvl1, workflowlevel2=wflvl2)

        request.user = self.tola_user.user
        view = DocumentationViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class DocumentationCreateViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_create_documentation_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.post('/api/documentation/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail', kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/documentation/', data)
        request.user = self.tola_user.user
        view = DocumentationViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['workflowlevel1'], wflvl1_url)

    def test_create_documentation_program_admin(self):
        request = self.factory.post('/api/documentation/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail', kwargs={'pk': wflvl1.id},
                             request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        data = {'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/documentation/', data)
        request.user = self.tola_user.user
        view = DocumentationViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['workflowlevel1'], wflvl1_url)

    def test_create_documentation_program_admin_json(self):
        request = self.factory.post('/api/documentation/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail', kwargs={'pk': wflvl1.id},
                             request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        data = {'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/documentation/', json.dumps(data),
                                    content_type='application/json')
        request.user = self.tola_user.user
        view = DocumentationViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['workflowlevel1'], wflvl1_url)


class DocumentationDeleteViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_delete_documentation_non_existing(self):
        request = self.factory.delete('/api/documentation/')
        request.user = self.tola_user.user
        view = DocumentationViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=288)
        self.assertEquals(response.status_code, 404)

    def test_delete_documentation_superuser(self):
        self.tola_user.user.is_superuser = True
        self.tola_user.user.is_staff = True
        self.tola_user.user.save()
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        documentation = factories.Documentation(workflowlevel1=wflvl1)
        request = self.factory.delete('/api/documentation/')
        request.user = self.tola_user.user
        view = DocumentationViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=documentation.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Documentation.DoesNotExist,
            Documentation.objects.get, pk=documentation.pk)

    def test_delete_documentation_org_admin(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        documentation = factories.Documentation(workflowlevel1=wflvl1)
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.delete('/api/documentation/')
        request.user = self.tola_user.user
        view = DocumentationViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=documentation.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Documentation.DoesNotExist,
            Documentation.objects.get, pk=documentation.pk)

    def test_delete_documentation_diff_org_org_admin(self):
        another_org = factories.Organization(name='Another Org')
        wflvl1 = factories.WorkflowLevel1(organization=another_org)
        documentation = factories.Documentation(workflowlevel1=wflvl1)
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.delete('/api/documentation/')
        request.user = self.tola_user.user
        view = DocumentationViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=documentation.pk)
        self.assertEquals(response.status_code, 403)
        Documentation.objects.get(pk=documentation.pk)

    def test_delete_documentation_program_admin(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        documentation = factories.Documentation(workflowlevel1=wflvl1)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        request = self.factory.delete('/api/documentation/')
        request.user = self.tola_user.user
        view = DocumentationViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=documentation.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Documentation.DoesNotExist,
            Documentation.objects.get, pk=documentation.pk)

    def test_delete_documentation_diff_org_program_admin(self):
        another_org = factories.Organization(name='Another Org')
        wflvl1 = factories.WorkflowLevel1(organization=another_org)
        documentation = factories.Documentation(workflowlevel1=wflvl1)
        group_org_admin = factories.Group(name=ROLE_PROGRAM_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.delete('/api/documentation/')
        request.user = self.tola_user.user
        view = DocumentationViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=documentation.pk)
        self.assertEquals(response.status_code, 403)
        Documentation.objects.get(pk=documentation.pk)

    def test_delete_documentation_normal_user(self):
        wflvl1 = factories.WorkflowLevel1()
        documentation = factories.Documentation(workflowlevel1=wflvl1)

        request = self.factory.delete('/api/documentation/')
        request.user = self.tola_user.user
        view = DocumentationViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=documentation.pk)
        self.assertEquals(response.status_code, 403)
        Documentation.objects.get(pk=documentation.pk)


class DocumentationFilterViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_filter_documentation_country_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        wflvl1_1 = factories.WorkflowLevel1(
            name='WorkflowLevel1_1',
            organization=self.tola_user.organization)
        wflvl2_1 = factories.WorkflowLevel2(workflowlevel1=wflvl1_1)
        WorkflowTeam.objects.create(workflow_user=self.tola_user,
                                    workflowlevel1=wflvl1_1)
        documentation1 = factories.Documentation(name='Document 1',
                                                 workflowlevel1=wflvl1_1,
                                                 workflowlevel2=wflvl2_1)

        another_org = factories.Organization(name='Another Org')
        wflvl1_2 = factories.WorkflowLevel1(
            name='WorkflowLevel1_2',
            organization=another_org)
        wflvl2_2 = factories.WorkflowLevel2(workflowlevel1=wflvl1_2)
        WorkflowTeam.objects.create(workflow_user=self.tola_user,
                                    workflowlevel1=wflvl1_2)
        factories.Documentation(name='Document 2', workflowlevel1=wflvl1_2,
                                workflowlevel2=wflvl2_2)

        request = self.factory.get(
            '/api/documentation'
            '/?workflowlevel2__workflowlevel1__organization__id=%s' %
            self.tola_user.organization.pk)
        request.user = self.tola_user.user
        view = DocumentationViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], documentation1.name)

    def test_filter_documentation_org_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        country1 = factories.Country()
        wflvl1_1 = factories.WorkflowLevel1(
            name='WorkflowLevel1_1',
            country=[country1],
            organization=self.tola_user.organization)
        wflvl2_1 = factories.WorkflowLevel2(workflowlevel1=wflvl1_1)
        WorkflowTeam.objects.create(workflow_user=self.tola_user,
                                    workflowlevel1=wflvl1_1)
        documentation1 = factories.Documentation(name='Document 1',
                                                 workflowlevel1=wflvl1_1,
                                                 workflowlevel2=wflvl2_1)

        country2 = factories.Country(country='Brazil', code='BR')
        wflvl1_2 = factories.WorkflowLevel1(
            name='WorkflowLevel1_2',
            country=[country2],
            organization=self.tola_user.organization)
        wflvl2_2 = factories.WorkflowLevel2(workflowlevel1=wflvl1_2)
        WorkflowTeam.objects.create(workflow_user=self.tola_user,
                                    workflowlevel1=wflvl1_2)
        factories.Documentation(name='Document 2', workflowlevel1=wflvl1_2,
                                workflowlevel2=wflvl2_2)

        request = self.factory.get(
            '/api/documentation'
            '/?workflowlevel2__workflowlevel1__country__country=%s' %
            country1.country)
        request.user = self.tola_user.user
        view = DocumentationViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], documentation1.name)
