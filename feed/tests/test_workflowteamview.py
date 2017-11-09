from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

import factories
from feed.views import WorkflowTeamViewSet
from workflow.models import (WorkflowTeam, ROLE_ORGANIZATION_ADMIN,
                             ROLE_PROGRAM_ADMIN, ROLE_PROGRAM_TEAM,
                             ROLE_VIEW_ONLY)


class WorkflowTeamListViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

        user_ringo = factories.User(first_name='Ringo', last_name='Starr')
        tola_user_ringo = factories.TolaUser(
            user=user_ringo, organization=self.tola_user.organization)
        self.wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        factories.WorkflowTeam(workflow_user=tola_user_ringo,
                               workflowlevel1=self.wflvl1,
                               partner_org=self.wflvl1.organization,
                               role=factories.Group(name=ROLE_VIEW_ONLY))

    def test_list_workflowteam_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        view = WorkflowTeamViewSet.as_view({'get': 'list'})
        request_get = self.factory.get('/api/workflowteam/')
        request_get.user = self.tola_user.user
        response = view(request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_workflowteam_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        # Create a user belonging to other Project in other Org
        user_george = factories.User(first_name='George', last_name='Harrison')
        tola_user_george = factories.TolaUser(
            user=user_george, organization=factories.Organization())
        wflvl1_other = factories.WorkflowLevel1(
            organization=tola_user_george.organization)
        factories.WorkflowTeam(workflow_user=tola_user_george,
                               workflowlevel1=wflvl1_other,
                               partner_org=wflvl1_other.organization,
                               role=factories.Group(name=ROLE_VIEW_ONLY))

        request_get = self.factory.get('/api/workflowteam/')
        request_get.user = self.tola_user.user
        view = WorkflowTeamViewSet.as_view({'get': 'list'})
        response = view(request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_workflowteam_program_admin(self):
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user, workflowlevel1=self.wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        request_get = self.factory.get('/api/workflowteam/')
        request_get.user = self.tola_user.user
        view = WorkflowTeamViewSet.as_view({'get': 'list'})
        response = view(request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_workflowteam_program_team(self):
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user, workflowlevel1=self.wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))

        request_get = self.factory.get('/api/workflowteam/')
        request_get.user = self.tola_user.user
        view = WorkflowTeamViewSet.as_view({'get': 'list'})
        response = view(request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_workflowteam_view_only(self):
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user, workflowlevel1=self.wflvl1,
            role=factories.Group(name=ROLE_VIEW_ONLY))

        request_get = self.factory.get('/api/workflowteam/')
        request_get.user = self.tola_user.user
        view = WorkflowTeamViewSet.as_view({'get': 'list'})
        response = view(request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_workflowteam_normaluser(self):
        request_get = self.factory.get('/api/workflowteam/')
        request_get.user = self.tola_user.user
        view = WorkflowTeamViewSet.as_view({'get': 'list'})
        response = view(request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)


class WorkflowTeamCreateViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        self.wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)

    def test_create_workflowteam_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': self.wflvl1.id})
        tolauser_url = reverse('tolauser-detail',
                               kwargs={'pk': self.tola_user.id})
        role = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        role_url = reverse('group-detail', kwargs={'pk': role.id})
        data = {
            'role': role_url,
            'workflow_user': tolauser_url,
            'workflowlevel1': wflvl1_url,
        }

        request = self.factory.post(None, data)
        request.user = self.tola_user.user
        view = WorkflowTeamViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)

        WorkflowTeam.objects.get(
            workflowlevel1=self.wflvl1,
            workflow_user=self.tola_user,
            role=role,
        )

    def test_create_workflowteam_org_admin(self):
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user, workflowlevel1=self.wflvl1,
            role=factories.Group(name=ROLE_ORGANIZATION_ADMIN))

        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': self.wflvl1.id})
        user_george = factories.User(first_name='George', last_name='Harrison')
        tola_user_george = factories.TolaUser(
            user=user_george, organization=factories.Organization())
        tolauser_url = reverse('tolauser-detail',
                               kwargs={'pk': tola_user_george.id})
        role = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        role_url = reverse('group-detail', kwargs={'pk': role.id})
        data = {
            'role': role_url,
            'workflow_user': tolauser_url,
            'workflowlevel1': wflvl1_url,
        }

        request = self.factory.post(None, data)
        request.user = self.tola_user.user
        view = WorkflowTeamViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)

        WorkflowTeam.objects.get(
            workflowlevel1=self.wflvl1,
            workflow_user=tola_user_george,
            role=role,
        )

    def test_create_workflowteam_program_admin(self):
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user, workflowlevel1=self.wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': self.wflvl1.id})
        tolauser_url = reverse('tolauser-detail',
                               kwargs={'pk': self.tola_user.id})
        role = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        role_url = reverse('group-detail', kwargs={'pk': role.id})
        data = {
            'role': role_url,
            'workflow_user': tolauser_url,
            'workflowlevel1': wflvl1_url,
        }

        request = self.factory.post(None, data)
        request.user = self.tola_user.user
        view = WorkflowTeamViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)

        WorkflowTeam.objects.get(
            workflowlevel1=self.wflvl1,
            workflow_user=self.tola_user,
            role=role,
        )

    def test_create_workflowteam_other_user(self):
        role_without_benefits = ROLE_PROGRAM_TEAM
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user, workflowlevel1=self.wflvl1,
            role=factories.Group(name=role_without_benefits))

        wflvl1_url = reverse('workflowlevel1-detail',
                             kwargs={'pk': self.wflvl1.id})
        tolauser_url = reverse('tolauser-detail',
                               kwargs={'pk': self.tola_user.id})
        role = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        role_url = reverse('group-detail', kwargs={'pk': role.id})
        data = {
            'role': role_url,
            'workflow_user': tolauser_url,
            'workflowlevel1': wflvl1_url,
        }

        request = self.factory.post(None, data)
        request.user = self.tola_user.user
        view = WorkflowTeamViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 403)

        self.assertRaises(
            WorkflowTeam.DoesNotExist,
            WorkflowTeam.objects.get, workflowlevel1=self.wflvl1,
            workflow_user=self.tola_user,
            role=role,
        )
