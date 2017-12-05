from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import ProfileTypeViewSet
from workflow.models import WorkflowTeam, ROLE_ORGANIZATION_ADMIN, \
    ROLE_PROGRAM_TEAM, ROLE_PROGRAM_ADMIN, ROLE_VIEW_ONLY


class ProfileTypeListViewsTest(TestCase):
    def setUp(self):
        factories.Organization(id=1)
        factories.ProfileType.create_batch(2)
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_list_profiletype_superuser(self):
        request = self.factory.get('/api/profiletype/')
        request.user = factories.User.build(is_superuser=True,
                                            is_staff=True)
        view = ProfileTypeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_profiletype_org_admin(self):
        request = self.factory.get('/api/profiletype/')
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request.user = self.tola_user.user
        view = ProfileTypeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.ProfileType(organization=self.tola_user.organization)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_profiletype_program_admin(self):
        request = self.factory.get('/api/profiletype/')
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        request.user = self.tola_user.user
        view = ProfileTypeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.ProfileType(organization=self.tola_user.organization)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_profiletype_program_team(self):
        request = self.factory.get('/api/profiletype/')
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))
        request.user = self.tola_user.user
        view = ProfileTypeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.ProfileType(organization=self.tola_user.organization)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_profiletype_view_only(self):
        request = self.factory.get('/api/profiletype/')
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            role=factories.Group(name=ROLE_VIEW_ONLY))
        request.user = self.tola_user.user
        view = ProfileTypeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        factories.ProfileType(organization=self.tola_user.organization)
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class ProfileTypeFilterViewsTest(TestCase):
    def setUp(self):
        factories.Organization(id=1)
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_filter_profiletype_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        p_type1 = factories.ProfileType(
            organization=self.tola_user.organization)
        p_type2 = factories.ProfileType(profile='Camp Site')
        request = self.factory.get('/api/profiletype/?organization__id=%s' %
                                   self.tola_user.organization.pk)
        request.user = self.tola_user.user
        view = ProfileTypeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['profile'], p_type1.profile)
        self.assertNotEqual(response.data[0]['profile'], p_type2.profile)
