import logging
import os

try:
    from chargebee import Addon, Subscription
except ImportError:
    pass
from django.test import TestCase, tag
from mock import Mock

import factories
from tola import DEMO_BRANCH
from tola.management.commands.loadinitialdata import DEFAULT_WORKFLOW_LEVEL_1S
from workflow.models import (Organization, WorkflowTeam, ROLE_PROGRAM_ADMIN,
                             ROLE_ORGANIZATION_ADMIN, ROLE_VIEW_ONLY)


@tag('pkg')
class AddUsersToDefaultWorkflowLevel1Test(TestCase):
    def setUp(self):
        logging.disable(logging.ERROR)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_not_demo_env(self):
        factories.TolaUser()  # triggers the signal
        self.assertEqual(WorkflowTeam.objects.all().count(), 0)

    def test_demo_env_no_wflvl1_matching(self):
        os.environ['APP_BRANCH'] = DEMO_BRANCH
        factories.WorkflowLevel1(name=DEFAULT_WORKFLOW_LEVEL_1S[0][1])
        factories.TolaUser()  # triggers the signal
        self.assertEqual(WorkflowTeam.objects.all().count(), 0)

        factories.WorkflowLevel1(name=DEFAULT_WORKFLOW_LEVEL_1S[1][1])
        factories.TolaUser(
            user=factories.User(first_name='George', last_name='Harrison')
        )  # triggers the signal
        self.assertEqual(WorkflowTeam.objects.all().count(), 0)

        factories.WorkflowLevel1(id=DEFAULT_WORKFLOW_LEVEL_1S[0][0], name='Any')
        factories.TolaUser(
            user=factories.User(first_name='Ringo', last_name='Starr')
        )  # triggers the signal
        self.assertEqual(WorkflowTeam.objects.all().count(), 0)

        factories.WorkflowLevel1(id=DEFAULT_WORKFLOW_LEVEL_1S[1][0], name='Any')
        factories.TolaUser(
            user=factories.User(first_name='Paul', last_name='McCartney')
        )  # triggers the signal
        self.assertEqual(WorkflowTeam.objects.all().count(), 0)

        os.environ['APP_BRANCH'] = ''

    def test_demo_workflowteam_assignment(self):
        os.environ['APP_BRANCH'] = DEMO_BRANCH
        role = factories.Group(name=ROLE_VIEW_ONLY)
        wflvl1_1 = factories.WorkflowLevel1(
            id=DEFAULT_WORKFLOW_LEVEL_1S[0][0],
            name=DEFAULT_WORKFLOW_LEVEL_1S[0][1])
        wflvl1_2 = factories.WorkflowLevel1(
            id=DEFAULT_WORKFLOW_LEVEL_1S[1][0],
            name=DEFAULT_WORKFLOW_LEVEL_1S[1][1])

        tola_user = factories.TolaUser(
            user=factories.User(first_name='Ringo', last_name='Starr')
        )  # triggers the signal
        WorkflowTeam.objects.get(
            workflow_user=tola_user, role=role, workflowlevel1=wflvl1_1)
        WorkflowTeam.objects.get(
            workflow_user=tola_user, role=role, workflowlevel1=wflvl1_2)
        os.environ['APP_BRANCH'] = ''

    def test_demo_workflowteam_assignment_not_reassigned_on_update(self):
        os.environ['APP_BRANCH'] = DEMO_BRANCH
        role = factories.Group(name=ROLE_VIEW_ONLY)
        wflvl1_0 = factories.WorkflowLevel1(
            id=DEFAULT_WORKFLOW_LEVEL_1S[0][0],
            name=DEFAULT_WORKFLOW_LEVEL_1S[0][1])
        wflvl1_1 = factories.WorkflowLevel1(
            id=DEFAULT_WORKFLOW_LEVEL_1S[1][0],
            name=DEFAULT_WORKFLOW_LEVEL_1S[1][1])


        tola_user = factories.TolaUser(
            user=factories.User(first_name='Ringo', last_name='Starr')
        )  # triggers the signal
        tola_user.name = 'Laura Pausini'
        tola_user.save()

        num_results = WorkflowTeam.objects.filter(
            workflow_user=tola_user, role=role, workflowlevel1=wflvl1_0).count()
        self.assertEqual(num_results, 1)
        num_results = WorkflowTeam.objects.filter(
            workflow_user=tola_user, role=role, workflowlevel1=wflvl1_1).count()
        self.assertEqual(num_results, 1)
        os.environ['APP_BRANCH'] = ''


class CheckSeatsSaveWFTeamsTest(TestCase):
    class ExternalResponse:
        def __init__(self, values):
            self.subscription = Subscription(values)
            self.subscription.status = 'active'

            addon = Addon(values)
            addon.id = 'user'
            addon.quantity = 0
            self.subscription.addons = [addon]

    def setUp(self):
        logging.disable(logging.ERROR)
        self.group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.group_program_admin = factories.Group(name=ROLE_PROGRAM_ADMIN)
        self.group_view_only = factories.Group(name=ROLE_VIEW_ONLY)
        self.org = factories.Organization(chargebee_subscription_id='12345')
        self.tola_user = factories.TolaUser(organization=self.org)

    def test_check_seats_save_team_increase(self):
        external_response = self.ExternalResponse(None)
        Subscription.retrieve = Mock(return_value=external_response)
        wflvl1_1 = factories.WorkflowLevel1(name='WorkflowLevel1_1')
        wflvl1_2 = factories.WorkflowLevel1(name='WorkflowLevel1_2')
        factories.WorkflowTeam(workflow_user=self.tola_user,
                               workflowlevel1=wflvl1_1,
                               role=self.group_program_admin)

        # It should increase the seats because the user doesn't
        # have any seat reserved for him
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 1)

        # It shouldn't increase the seats because the user already
        # has a seat reserved for him
        factories.WorkflowTeam(workflow_user=self.tola_user,
                               workflowlevel1=wflvl1_2,
                               role=self.group_program_admin)
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 1)

    def test_check_seats_save_team_decrease(self):
        external_response = self.ExternalResponse(None)
        Subscription.retrieve = Mock(return_value=external_response)
        wflvl1_1 = factories.WorkflowLevel1(name='WorkflowLevel1_1')
        wflvl1_2 = factories.WorkflowLevel1(name='WorkflowLevel1_2')
        wfteam1_1 = factories.WorkflowTeam(workflow_user=self.tola_user,
                                           workflowlevel1=wflvl1_1,
                                           role=self.group_program_admin)
        wfteam1_2 = factories.WorkflowTeam(workflow_user=self.tola_user,
                                           workflowlevel1=wflvl1_2,
                                           role=self.group_program_admin)

        # It shouldn't increase the amount of used seats
        # the user already has a WorkflowTeam
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 1)

        # It shouldn't decrease the seats because the user still has
        # another WorkflowTeam
        wfteam1_1.role = self.group_view_only
        wfteam1_1.save()
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 1)

        # It should decrease the seats because the user isn't Org Admin
        # and doesn't have another WorkflowTeam
        wfteam1_2.role = self.group_view_only
        wfteam1_2.save()
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 0)

    def test_check_seats_save_team_without_subscription(self):
        external_response = self.ExternalResponse(None)
        Subscription.retrieve = Mock(return_value=external_response)
        self.tola_user.organization = factories.Organization()
        wflvl1 = factories.WorkflowLevel1(name='WorkflowLevel1')
        factories.WorkflowTeam(workflow_user=self.tola_user,
                               workflowlevel1=wflvl1,
                               role=self.group_program_admin)

        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 0)

    def test_check_seats_save_team_demo(self):
        os.environ['APP_BRANCH'] = DEMO_BRANCH
        self.tola_user.organization = factories.Organization()
        wflvl1 = factories.WorkflowLevel1(name='WorkflowLevel1')
        factories.WorkflowTeam(workflow_user=self.tola_user,
                               workflowlevel1=wflvl1,
                               role=self.group_program_admin)

        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 0)
        os.environ['APP_BRANCH'] = ''

    def test_check_seats_save_team_org_admin(self):
        # When a user is an org admin, the seat has to be updated with the
        # user groups signal, that's why it shouldn't be changed in this case.
        self.tola_user.user.groups.add(self.group_org_admin)
        self.tola_user.user.save()

        external_response = self.ExternalResponse(None)
        Subscription.retrieve = Mock(return_value=external_response)
        wflvl1 = factories.WorkflowLevel1(name='WorkflowLevel1')
        factories.WorkflowTeam(workflow_user=self.tola_user,
                               workflowlevel1=wflvl1,
                               role=self.group_program_admin)

        # It should have only one seat because of the Org Admin role
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 1)


class CheckSeatsDeleteWFTeamsTest(TestCase):
    class ExternalResponse:
        def __init__(self, values):
            self.subscription = Subscription(values)
            self.subscription.status = 'active'

            addon = Addon(values)
            addon.id = 'user'
            addon.quantity = 0
            self.subscription.addons = [addon]

    def setUp(self):
        logging.disable(logging.ERROR)
        self.group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.group_program_admin = factories.Group(name=ROLE_PROGRAM_ADMIN)
        self.org = factories.Organization(chargebee_subscription_id='12345')
        self.tola_user = factories.TolaUser(organization=self.org)

    def test_check_seats_delete_team_decrease(self):
        external_response = self.ExternalResponse(None)
        Subscription.retrieve = Mock(return_value=external_response)
        wflvl1 = factories.WorkflowLevel1(name='WorkflowLevel1')
        wfteam = factories.WorkflowTeam(workflow_user=self.tola_user,
                                        workflowlevel1=wflvl1,
                                        role=self.group_program_admin)

        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 1)

        wfteam.delete()
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 0)

    def test_check_seats_save_team_not_decrease(self):
        external_response = self.ExternalResponse(None)
        Subscription.retrieve = Mock(return_value=external_response)
        wflvl1_1 = factories.WorkflowLevel1(name='WorkflowLevel1_1')
        wflvl1_2 = factories.WorkflowLevel1(name='WorkflowLevel1_2')
        wfteam1_1 = factories.WorkflowTeam(workflow_user=self.tola_user,
                                           workflowlevel1=wflvl1_1,
                                           role=self.group_program_admin)
        factories.WorkflowTeam(workflow_user=self.tola_user,
                               workflowlevel1=wflvl1_2,
                               role=self.group_program_admin)

        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 1)

        wfteam1_1.delete()
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 1)

    def test_check_seats_save_team_demo(self):
        os.environ['APP_BRANCH'] = DEMO_BRANCH
        self.tola_user.organization = factories.Organization()
        wflvl1 = factories.WorkflowLevel1(name='WorkflowLevel1')
        factories.WorkflowTeam(workflow_user=self.tola_user,
                               workflowlevel1=wflvl1,
                               role=self.group_program_admin)

        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 0)
        os.environ['APP_BRANCH'] = ''

    def test_check_seats_save_team_org_admin(self):
        external_response = self.ExternalResponse(None)
        Subscription.retrieve = Mock(return_value=external_response)
        self.tola_user.user.groups.add(self.group_org_admin)
        self.tola_user.user.save()

        wflvl1 = factories.WorkflowLevel1(name='WorkflowLevel1')
        wfteam = factories.WorkflowTeam(workflow_user=self.tola_user,
                                        workflowlevel1=wflvl1,
                                        role=self.group_program_admin)

        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 1)

        wfteam.delete()
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 1)


class CheckSeatsSaveUserGroupTest(TestCase):
    class ExternalResponse:
        def __init__(self, values):
            self.subscription = Subscription(values)
            self.subscription.status = 'active'

            addon = Addon(values)
            addon.id = 'user'
            addon.quantity = 0
            self.subscription.addons = [addon]

    def setUp(self):
        logging.disable(logging.ERROR)
        self.group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.group_view_only = factories.Group(name=ROLE_VIEW_ONLY)
        self.org = factories.Organization(chargebee_subscription_id='12345')
        self.tola_user = factories.TolaUser(organization=self.org)

    def test_check_seats_save_user_groups_increase(self):
        external_response = self.ExternalResponse(None)
        Subscription.retrieve = Mock(return_value=external_response)

        self.tola_user.user.groups.add(self.group_org_admin)
        self.tola_user.user.save()

        # It should have only one seat because of the Org Admin role
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 1)

    def test_check_seats_save_user_groups_decrease(self):
        external_response = self.ExternalResponse(None)
        Subscription.retrieve = Mock(return_value=external_response)

        self.tola_user.user.groups.add(self.group_org_admin)
        self.tola_user.user.save()

        # It should have only one seat because of the Org Admin role
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 1)

        self.tola_user.user.groups.add(self.group_view_only)
        self.tola_user.user.save()

        # The user doesn't have any WorkflowTeam and isn't Org Admin anymore
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 0)

    def test_check_seats_save_user_groups_without_subscription(self):
        external_response = self.ExternalResponse(None)
        Subscription.retrieve = Mock(return_value=external_response)

        self.tola_user.organization = factories.Organization()
        self.tola_user.save()

        self.tola_user.user.groups.add(self.group_org_admin)
        self.tola_user.user.save()

        # It should have only one seat because of the Org Admin role
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 0)

    def test_check_seats_save_user_groups_demo(self):
        os.environ['APP_BRANCH'] = DEMO_BRANCH
        self.tola_user.organization = factories.Organization()
        self.tola_user.save()

        self.tola_user.user.groups.add(self.group_org_admin)
        self.tola_user.user.save()

        # It should have only one seat because of the Org Admin role
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 0)
        os.environ['APP_BRANCH'] = ''
