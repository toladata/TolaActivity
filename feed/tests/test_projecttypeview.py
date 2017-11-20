from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import ProjectTypeViewSet
from workflow.models import WorkflowTeam, ROLE_ORGANIZATION_ADMIN, \
    ROLE_PROGRAM_TEAM, ROLE_PROGRAM_ADMIN, ROLE_VIEW_ONLY


class ProjectTypeListViewsTest(TestCase):
    def setUp(self):
        factories.Organization(id=1)
        factories.ProjectType.create_batch(2)
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_list_projecttype_superuser(self):
        request = self.factory.get('/api/projecttype/')
        request.user = factories.User.build(is_superuser=True,
                                            is_staff=True)
        view = ProjectTypeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_projecttype_org_admin(self):
        request = self.factory.get('/api/projecttype/')
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request.user = self.tola_user.user
        view = ProjectTypeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.ProjectType(organization=self.tola_user.organization)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_projecttype_program_admin(self):
        request = self.factory.get('/api/projecttype/')
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        request.user = self.tola_user.user
        view = ProjectTypeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.ProjectType(organization=self.tola_user.organization)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_projecttype_program_team(self):
        request = self.factory.get('/api/projecttype/')
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))
        request.user = self.tola_user.user
        view = ProjectTypeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.ProjectType(organization=self.tola_user.organization)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_projecttype_view_only(self):
        request = self.factory.get('/api/projecttype/')
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            role=factories.Group(name=ROLE_VIEW_ONLY))
        request.user = self.tola_user.user
        view = ProjectTypeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.ProjectType(organization=self.tola_user.organization)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class ProjectTypeFilterViewTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()
        self.factory = APIRequestFactory()

    def test_filter_projecttype_superuser(self):
        another_org = factories.Organization(name='Another Org')
        projecttype1_1 = factories.ProjectType(
            organization=self.tola_user.organization)
        factories.ProjectType(
            name='Another ProjectType',
            organization=another_org)

        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.get('/api/projecttype/?organization__id=%s' %
                                   self.tola_user.organization.pk)
        request.user = self.tola_user.user
        view = ProjectTypeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], projecttype1_1.name)

    def test_filter_projecttype_normaluser(self):
        another_org = factories.Organization(name='Another Org')
        projecttype1_1 = factories.ProjectType(
            organization=self.tola_user.organization)
        factories.ProjectType(
            name='Another ProjectType',
            organization=another_org)

        request = self.factory.get('/api/projecttype/?organization__id=%s' %
                                   self.tola_user.organization.pk)
        request.user = self.tola_user.user
        view = ProjectTypeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], projecttype1_1.name)
