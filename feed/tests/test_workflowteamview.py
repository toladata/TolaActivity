from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import WorkflowTeamViewSet
from workflow.models import (WorkflowTeam, ROLE_ORGANIZATION_ADMIN,
                             ROLE_PROGRAM_ADMIN, ROLE_PROGRAM_TEAM,
                             ROLE_VIEW_ONLY)


class WorkflowTeamViewsTest(TestCase):
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

        self.factory = APIRequestFactory()

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
