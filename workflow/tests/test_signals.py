import json
import logging
import os

from chargebee import APIError
from chargebee.models import Subscription
from django.core import mail
from django.test import TestCase, override_settings, tag
from mock import Mock, patch

import factories
from tola import DEMO_BRANCH, PRODUCTION_BRANCH, STAGING_BRANCH
from tola.management.commands.loadinitialdata import DEFAULT_WORKFLOW_LEVEL_1S
from workflow.models import (Dashboard, Organization, WorkflowTeam,
                             ROLE_PROGRAM_ADMIN, ROLE_ORGANIZATION_ADMIN,
                             ROLE_VIEW_ONLY, ROLE_PROGRAM_TEAM,  WorkflowLevel1,
                             WorkflowLevel2, DEFAULT_PROGRAM_NAME)


@tag('pkg')
class AddUsersToDefaultWorkflowLevel1Test(TestCase):
    def setUp(self):
        os.environ['APP_BRANCH'] = ''
        logging.disable(logging.ERROR)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_not_demo_env(self):
        factories.TolaUser()  # triggers the signal
        self.assertEqual(WorkflowTeam.objects.all().count(), 0)

    @patch('workflow.signals.tsync')
    def test_demo_env_no_wflvl1_matching(self, mock_tsync):
        os.environ['APP_BRANCH'] = DEMO_BRANCH
        mock_tsync.create_instance.return_value = Mock()
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

    @patch('workflow.signals.tsync')
    def test_demo_workflowteam_assignment(self, mock_tsync):
        os.environ['APP_BRANCH'] = DEMO_BRANCH
        mock_tsync.create_instance.return_value = Mock()
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

    @patch('workflow.signals.tsync')
    def test_demo_workflowteam_assignment_not_reassigned_on_update(
            self, mock_tsync):
        os.environ['APP_BRANCH'] = DEMO_BRANCH
        mock_tsync.create_instance.return_value = Mock()
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


@tag('pkg')
class CreateDefaultProgramTest(TestCase):

    @override_settings(CREATE_DEFAULT_PROGRAM=False)
    def test_deactivated(self):
        factories.Organization()  # triggers the signal
        self.assertEqual(WorkflowLevel1.objects.all().count(), 0)

    @override_settings(CREATE_DEFAULT_PROGRAM=True)
    def test_activated(self):
        organization = factories.Organization()  # triggers the signal
        WorkflowLevel1.objects.get(name=DEFAULT_PROGRAM_NAME,
                                   organization=organization)

    @override_settings(CREATE_DEFAULT_PROGRAM=True)
    def test_activated_update(self):
        organization = factories.Organization()  # triggers the signal
        organization.name = 'Name updated'
        organization.save()
        self.assertEqual(WorkflowLevel1.objects.all().count(), 1)


@tag('pkg')
class AddTolaUserAsProgramAdminTest(TestCase):
    def setUp(self):
        os.environ['APP_BRANCH'] = ''
        logging.disable(logging.ERROR)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    @override_settings(SET_PROGRAM_ADMIN_DEFAULT=False)
    @override_settings(CREATE_DEFAULT_PROGRAM=False)
    def test_deactivated(self):
        factories.TolaUser()  # triggers the signal
        self.assertEqual(WorkflowTeam.objects.all().count(), 0)

    @override_settings(SET_PROGRAM_ADMIN_DEFAULT=True)
    @override_settings(CREATE_DEFAULT_PROGRAM=False)
    def test_activated_but_not_create_default_program(self):
        factories.TolaUser()  # triggers the signal
        self.assertEqual(WorkflowTeam.objects.all().count(), 0)

    @override_settings(SET_PROGRAM_ADMIN_DEFAULT=True)
    @override_settings(CREATE_DEFAULT_PROGRAM=True)
    def test_activated(self):
        role_program_admin = factories.Group(name=ROLE_PROGRAM_ADMIN)
        tolauser = factories.TolaUser()  # triggers the signal
        wft = WorkflowTeam.objects.get(workflow_user=tolauser)
        self.assertEqual(wft.role, role_program_admin)

    @override_settings(SET_PROGRAM_ADMIN_DEFAULT=True)
    @override_settings(CREATE_DEFAULT_PROGRAM=True)
    def test_activated_save_two_times(self):
        """
        When the TolaUser is saved, a WorkflowTeam object for that user and
        the default program is created only once.
        """
        role_program_admin = factories.Group(name=ROLE_PROGRAM_ADMIN)
        tolauser = factories.TolaUser()  # triggers the signal
        tolauser.save()  # triggers the signal again
        wft = WorkflowTeam.objects.get(workflow_user=tolauser)
        self.assertEqual(wft.role, role_program_admin)

    @override_settings(SET_PROGRAM_ADMIN_DEFAULT=True)
    @override_settings(CREATE_DEFAULT_PROGRAM=True)
    def test_activated_program_lowercase(self):
        """
        If the default program name is written in different case letters, the
        signal does not crash.
        """
        role_program_admin = factories.Group(name=ROLE_PROGRAM_ADMIN)
        tolauser = factories.TolaUser()  # triggers the signal
        wflvl1 = WorkflowLevel1.objects.get(name=DEFAULT_PROGRAM_NAME)
        wflvl1.name = DEFAULT_PROGRAM_NAME.lower()
        wflvl1.save()
        WorkflowTeam.objects.all().delete()

        tolauser.name = 'Any'
        tolauser.save()  # trigger again the signal
        wft = WorkflowTeam.objects.get(workflow_user=tolauser)
        self.assertEqual(wft.role, role_program_admin)


@tag('pkg')
class CheckSeatsSaveWFTeamsTest(TestCase):
    class ExternalResponse:
        def __init__(self, values):
            self.subscription = Subscription(values)
            self.subscription.status = 'active'
            self.subscription.plan_quantity = 1

    def setUp(self):
        os.environ['APP_BRANCH'] = ''
        logging.disable(logging.ERROR)
        self.group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.group_program_admin = factories.Group(name=ROLE_PROGRAM_ADMIN)
        self.group_program_team = factories.Group(name=ROLE_PROGRAM_TEAM)
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

    @patch('workflow.signals.tsync')
    def test_check_seats_save_team_demo(self, mock_tsync):
        os.environ['APP_BRANCH'] = DEMO_BRANCH
        mock_tsync.create_instance.return_value = Mock()
        self.tola_user.organization = factories.Organization()
        wflvl1 = factories.WorkflowLevel1(name='WorkflowLevel1')
        factories.WorkflowTeam(workflow_user=self.tola_user,
                               workflowlevel1=wflvl1,
                               role=self.group_program_admin)

        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 0)

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

    def test_check_seats_save_team_retrieve_subscription_fails(self):
        """
        The number of seats will be increased in the system but it's not
        possible to check the quantity of the plan because the retrieve
        failed.
        """
        self.tola_user.user.groups.add(self.group_org_admin)
        self.tola_user.user.save()
        self.org = Organization.objects.get(pk=self.org.id)
        user = factories.User(first_name='John', last_name='Lennon')
        tolauser = factories.TolaUser(user=user, organization=self.org)

        json_obj = {
            'message': "Sorry, we couldn't find that resource",
            'error_code': 'resource_not_found'
        }
        sub_response = APIError(404, json_obj)
        Subscription.retrieve = Mock(side_effect=sub_response)
        wflvl1 = factories.WorkflowLevel1(name='WorkflowLevel1')
        factories.WorkflowTeam(workflow_user=tolauser,
                               workflowlevel1=wflvl1,
                               role=self.group_program_admin)

        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 2)
        self.assertEqual(len(mail.outbox), 0)

@tag('pkg')
class CheckSeatsDeleteWFTeamsTest(TestCase):
    class ExternalResponse:
        def __init__(self, values):
            self.subscription = Subscription(values)
            self.subscription.status = 'active'
            self.subscription.plan_quantity = 1

    def setUp(self):
        os.environ['APP_BRANCH'] = ''
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

    def test_check_seats_delete_team_not_decrease(self):
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

    @patch('workflow.signals.tsync')
    def test_check_seats_save_team_demo(self, mock_tsync):
        os.environ['APP_BRANCH'] = DEMO_BRANCH
        mock_tsync.create_instance.return_value = Mock()
        self.tola_user.organization = factories.Organization()
        wflvl1 = factories.WorkflowLevel1(name='WorkflowLevel1')
        factories.WorkflowTeam(workflow_user=self.tola_user,
                               workflowlevel1=wflvl1,
                               role=self.group_program_admin)

        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 0)

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


@tag('pkg')
class CheckSeatsSaveUserGroupTest(TestCase):
    class ExternalResponse:
        def __init__(self, values):
            self.subscription = Subscription(values)
            self.subscription.status = 'active'
            self.subscription.plan_quantity = 1

    def setUp(self):
        os.environ['APP_BRANCH'] = ''
        logging.disable(logging.ERROR)
        self.group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.group_view_only = factories.Group(name=ROLE_VIEW_ONLY)
        self.group_program_admin = factories.Group(name=ROLE_PROGRAM_ADMIN)
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

        self.tola_user.user.groups.remove(self.group_org_admin)

        # The user doesn't have any WorkflowTeam and isn't Org Admin anymore
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 0)

    def test_check_seats_save_user_groups_viewonly_doent_affect(self):
        external_response = self.ExternalResponse(None)
        Subscription.retrieve = Mock(return_value=external_response)

        self.tola_user.user.groups.add(self.group_view_only)
        self.tola_user.user.save()

        # It should have only one seat because of the Org Admin role
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 0)

        self.tola_user.user.groups.remove(self.group_view_only)

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

    @patch('workflow.signals.tsync')
    def test_check_seats_save_user_groups_demo(self, mock_tsync):
        os.environ['APP_BRANCH'] = DEMO_BRANCH
        mock_tsync.create_instance.return_value = Mock()
        self.tola_user.organization = factories.Organization()
        self.tola_user.save()

        self.tola_user.user.groups.add(self.group_org_admin)
        self.tola_user.user.save()

        # It should have only one seat because of the Org Admin role
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 0)

    def test_check_seats_save_user_groups_retrieve_subscription_fails(self):
        """
        The number of seats will be increased in the system but it's not
        possible to check the quantity of the plan because the retrieve
        failed.
        """
        json_obj = {
            'message': "Sorry, we couldn't find that resource",
            'error_code': 'resource_not_found'
        }
        sub_response = APIError(404, json_obj)
        Subscription.retrieve = Mock(side_effect=sub_response)
        self.tola_user.user.groups.add(self.group_org_admin)
        self.tola_user.user.save()

        self.org = Organization.objects.get(pk=self.org.id)
        user = factories.User(first_name='John', last_name='Lennon')
        tolauser = factories.TolaUser(user=user, organization=self.org)
        tolauser.user.groups.add(self.group_org_admin)
        tolauser.user.save()

        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 2)
        self.assertEqual(len(mail.outbox), 0)

@tag('pkg')
class AddPublicUrlTokenTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()

    def test_add_public_url_token_create_not_public_url(self):
        dashboard = Dashboard.objects.create(user=self.tola_user)
        self.assertNotEqual(dashboard.public,
                            {'all': False, 'org': False, 'url': False})
        self.assertIsNone(dashboard.public_url_token)

    def test_add_public_url_token_create_public_url(self):
        dashboard = Dashboard.objects.create(
            user=self.tola_user,
            public={'all': False, 'org': False, 'url': True})
        self.assertEqual(dashboard.public,
                         {'all': False, 'org': False, 'url': True})
        self.assertIsNotNone(dashboard.public_url_token)

    def test_add_public_url_token_update_not_public_url(self):
        dashboard = Dashboard.objects.create(user=self.tola_user)
        dashboard.public = {'all': True, 'org': False, 'url': False}
        dashboard.save()

        self.assertEqual(dashboard.public,
                         {'all': True, 'org': False, 'url': False})
        self.assertIsNone(dashboard.public_url_token)

    def test_add_public_url_token_update_public_url(self):
        dashboard = Dashboard.objects.create(user=self.tola_user)
        dashboard.public = {'all': False, 'org': False, 'url': True}
        dashboard.save()

        self.assertEqual(dashboard.public,
                         {'all': False, 'org': False, 'url': True})
        self.assertIsNotNone(dashboard.public_url_token)

    def test_add_public_url_token_create_and_update(self):
        dashboard = Dashboard.objects.create(
            user=self.tola_user,
            public={'all': False, 'org': False, 'url': True})
        self.assertEqual(dashboard.public,
                         {'all': False, 'org': False, 'url': True})
        self.assertIsNotNone(dashboard.public_url_token)

        dashboard.public = {'all': True, 'org': False, 'url': False}
        dashboard.save()
        self.assertEqual(dashboard.public,
                         {'all': True, 'org': False, 'url': False})
        self.assertIsNone(dashboard.public_url_token)


@tag('pkg')
class SignalSyncTrackTest(TestCase):
    def setUp(self):
        factories.Group()
        self.tola_user = factories.TolaUser()

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @override_settings(TOLA_TRACK_SYNC_ENABLED=True)
    @patch('workflow.signals.tsync')
    def test_sync_save_create(self, mock_tsync):
        mock_tsync.create_instance.return_value = Mock()

        org = factories.Organization()
        mock_tsync.create_instance.assert_called_with(org)

        wfl1 = factories.WorkflowLevel1()
        mock_tsync.create_instance.assert_called_with(wfl1)

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @override_settings(TOLA_TRACK_SYNC_ENABLED=False)
    @patch('workflow.signals.tsync')
    def test_sync_save_create_disabled(self, mock_tsync):
        mock_tsync.create_instance.return_value = Mock()

        factories.Organization()
        self.assertFalse(mock_tsync.create_instance.called)

        factories.WorkflowLevel1()
        self.assertFalse(mock_tsync.create_instance.called)

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @override_settings(TOLA_TRACK_SYNC_ENABLED=True)
    @patch('workflow.signals.tsync')
    def test_sync_save_update(self, mock_tsync):
        mock_tsync.create_instance.return_value = Mock()
        mock_tsync.update_instance.return_value = Mock()

        org = factories.Organization()
        wfl1 = factories.WorkflowLevel1()

        org.name = 'Another Org'
        org.description = 'The Org name was changed'
        org.save()
        mock_tsync.update_instance.assert_called_with(org)

        wfl1.name = 'Another Program'
        wfl1.save()
        mock_tsync.update_instance.assert_called_with(wfl1)

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @override_settings(TOLA_TRACK_SYNC_ENABLED=False)
    @patch('workflow.signals.tsync')
    def test_sync_save_update_disabled(self, mock_tsync):
        mock_tsync.create_instance.return_value = Mock()
        mock_tsync.update_instance.return_value = Mock()

        org = factories.Organization()
        wfl1 = factories.WorkflowLevel1()

        org.name = 'Another Org'
        org.description = 'The Org name was changed'
        org.save()
        self.assertFalse(mock_tsync.update_instance.called)

        wfl1.name = 'Another Program'
        wfl1.save()
        self.assertFalse(mock_tsync.update_instance.called)

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @override_settings(TOLA_TRACK_SYNC_ENABLED=True)
    @patch('workflow.signals.tsync')
    def test_sync_save_delete(self, mock_tsync):
        mock_tsync.create_instance.return_value = Mock()
        mock_tsync.delete_instance.return_value = Mock()

        org = factories.Organization()
        wfl1 = factories.WorkflowLevel1()

        org.delete()
        mock_tsync.delete_instance.assert_called_with(org)

        wfl1.delete()
        mock_tsync.delete_instance.assert_called_with(wfl1)

    @override_settings(TOLA_TRACK_URL='https://tolatrack.com')
    @override_settings(TOLA_TRACK_TOKEN='TheToken')
    @override_settings(TOLA_TRACK_SYNC_ENABLED=False)
    @patch('workflow.signals.tsync')
    def test_sync_save_delete_disabled(self, mock_tsync):
        mock_tsync.create_instance.return_value = Mock()
        mock_tsync.delete_instance.return_value = Mock()

        org = factories.Organization()
        wfl1 = factories.WorkflowLevel1()

        org.delete()
        self.assertFalse(mock_tsync.delete_instance.called)

        wfl1.delete()
        self.assertFalse(mock_tsync.delete_instance.called)


@tag('pkg')
class BudgetSaveTest(TestCase):
    def setUp(self):
        self.organization = factories.Organization()
        self.user = factories.User()
        self.tola_user = factories.TolaUser(organization=self.organization)

    def test_save_budget_value_without_wfl2_create(self):
        """
        When a budget is created without wfl2s, it's should work properly
        """
        budget = factories.Budget(proposed_value=100, actual_value=10)

        self.assertEqual(budget.proposed_value, 100.00)
        self.assertEqual(budget.actual_value, 10.00)

    def test_save_budget_value_from_wfl2_create(self):
        """
        When a budget is created, the related wfl2s total_estimated_budget
        should be updated
        """

        wflvl1 = factories.WorkflowLevel1(name='WorkflowLevel1',
                                          organization=self.organization)
        wflvl2 = factories.WorkflowLevel2(name='WorkflowLevel2',
                                          workflowlevel1=wflvl1,
                                          total_estimated_budget=0,
                                          actual_cost=0)
        factories.Budget(proposed_value=100,
                         actual_value=10,
                         workflowlevel2=wflvl2)

        wflvl2 = WorkflowLevel2.objects.get(pk=wflvl2.pk)
        self.assertEqual(wflvl2.total_estimated_budget, 100.00)
        self.assertEqual(wflvl2.actual_cost, 10.00)

    def test_save_budget_value_from_wfl2_create_more(self):
        """
        When a budget is updated, the related wfl2s total_estimated_budget
        should be updated
        """

        wflvl1 = factories.WorkflowLevel1(name='WorkflowLevel1',
                                          organization=self.organization)
        wflvl2 = factories.WorkflowLevel2(name='WorkflowLevel2',
                                          workflowlevel1=wflvl1,
                                          total_estimated_budget=0,
                                          actual_cost=0)
        factories.Budget(proposed_value=100,
                         actual_value=10,
                         workflowlevel2=wflvl2)

        factories.Budget(proposed_value=80,
                         actual_value=20,
                         workflowlevel2=wflvl2)

        wflvl2 = WorkflowLevel2.objects.get(pk=wflvl2.pk)
        self.assertEqual(wflvl2.total_estimated_budget, 180.00)
        self.assertEqual(wflvl2.actual_cost, 30.00)

    def test_save_budget_value_from_wfl2_update(self):
        """
        When a budget is updated, the related wfl2s total_estimated_budget
        should be updated
        """

        wflvl1 = factories.WorkflowLevel1(name='WorkflowLevel1',
                                          organization=self.organization)
        wflvl2 = factories.WorkflowLevel2(name='WorkflowLevel2',
                                          workflowlevel1=wflvl1,
                                          total_estimated_budget=0,
                                          actual_cost=0)
        budget = factories.Budget(proposed_value=100,
                                  actual_value=10,
                                  workflowlevel2=wflvl2)

        budget.proposed_value = 150
        budget.actual_value = 50
        budget.save()

        wflvl2 = WorkflowLevel2.objects.get(pk=wflvl2.pk)
        self.assertEqual(wflvl2.total_estimated_budget, 150.00)
        self.assertEqual(wflvl2.actual_cost, 50.00)


@tag('pkg')
class BudgetDeleteTest(TestCase):
    def setUp(self):
        self.organization = factories.Organization()
        self.user = factories.User()
        self.tola_user = factories.TolaUser(organization=self.organization)

    def test_delete_budget_value_from_wfl2(self):
        """
        When budget deleted, then related wfl2s total_estimated_budget
        should be updated
        """

        wflvl1 = factories.WorkflowLevel1(name='WorkflowLevel1',
                                          organization=self.organization)
        wflvl2 = factories.WorkflowLevel2(name='WorkflowLevel2',
                                          workflowlevel1=wflvl1,
                                          total_estimated_budget=0,
                                          actual_cost=0)
        factories.Budget(proposed_value=100,
                         actual_value=10,
                         workflowlevel2=wflvl2)

        budget_2 = factories.Budget(proposed_value=80,
                                    actual_value=20,
                                    workflowlevel2=wflvl2)

        wflvl2 = WorkflowLevel2.objects.get(pk=wflvl2.pk)
        self.assertEqual(wflvl2.total_estimated_budget, 180.00)
        self.assertEqual(wflvl2.actual_cost, 30.00)

        budget_2.delete()
        wflvl2 = WorkflowLevel2.objects.get(pk=wflvl2.pk)
        self.assertEqual(wflvl2.total_estimated_budget, 100.00)
        self.assertEqual(wflvl2.actual_cost, 10.00)
