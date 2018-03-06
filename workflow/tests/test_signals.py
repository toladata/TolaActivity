import logging
import os

try:
    from chargebee import Addon, Subscription
except ImportError:
    pass
from django.core import mail
from django.test import TestCase, override_settings, tag
from mock import Mock, patch

import factories
from tola import DEMO_BRANCH
from tola.management.commands.loadinitialdata import DEFAULT_WORKFLOW_LEVEL_1S
from workflow.models import (Organization, WorkflowTeam, ROLE_PROGRAM_ADMIN,
                             ROLE_ORGANIZATION_ADMIN, ROLE_VIEW_ONLY)


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


class CheckSeatsSaveWFTeamsTest(TestCase):
    class ExternalResponse:
        def __init__(self, values):
            self.subscription = Subscription(values)
            self.subscription.status = 'active'

            addon = Addon(values)
            addon.id = 'user'
            addon.quantity = 1
            self.subscription.addons = [addon]

    def setUp(self):
        os.environ['APP_BRANCH'] = ''
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

    @override_settings(DEFAULT_REPLY_TO='noreply@test.com')
    def test_check_seats_save_team_exceed_notify(self):
        self.tola_user.user.groups.add(self.group_org_admin)
        self.tola_user.user.save()
        self.org = Organization.objects.get(pk=self.org.id)
        user = factories.User(first_name='John', last_name='Lennon')
        tolauser = factories.TolaUser(user=user, organization=self.org)

        external_response = self.ExternalResponse(None)
        Subscription.retrieve = Mock(return_value=external_response)
        wflvl1 = factories.WorkflowLevel1(name='WorkflowLevel1')
        factories.WorkflowTeam(workflow_user=tolauser,
                               workflowlevel1=wflvl1,
                               role=self.group_program_admin)

        # It should notify the OrgAdmin
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 2)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Exceeded the number of editors', mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].to, [user.email])
        self.assertEqual(mail.outbox[0].reply_to, ['noreply@test.com'])
        self.assertEqual(mail.outbox[0].body,
                         'The number of editors has exceeded the amount of '
                         'users set in your Subscription. Please check it '
                         'out!\nCurrent amount of editors: 2.\nSelected '
                         'amount of editors: 1.')


class CheckSeatsDeleteWFTeamsTest(TestCase):
    class ExternalResponse:
        def __init__(self, values):
            self.subscription = Subscription(values)
            self.subscription.status = 'active'

            addon = Addon(values)
            addon.id = 'user'
            addon.quantity = 1
            self.subscription.addons = [addon]

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


class CheckSeatsSaveUserGroupTest(TestCase):
    class ExternalResponse:
        def __init__(self, values):
            self.subscription = Subscription(values)
            self.subscription.status = 'active'

            addon = Addon(values)
            addon.id = 'user'
            addon.quantity = 1
            self.subscription.addons = [addon]

    def setUp(self):
        os.environ['APP_BRANCH'] = ''
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

    @override_settings(DEFAULT_REPLY_TO='noreply@test.com')
    def test_check_seats_save_user_groups_exceed_notify(self):
        external_response = self.ExternalResponse(None)
        Subscription.retrieve = Mock(return_value=external_response)
        self.tola_user.user.groups.add(self.group_org_admin)
        self.tola_user.user.save()

        self.org = Organization.objects.get(pk=self.org.id)
        user = factories.User(first_name='John', last_name='Lennon')
        tolauser = factories.TolaUser(user=user, organization=self.org)
        tolauser.user.groups.add(self.group_org_admin)
        tolauser.user.save()

        # It should notify the OrgAdmin
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 2)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Exceeded the number of editors', mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].to, [user.email])
        self.assertEqual(mail.outbox[0].reply_to, ['noreply@test.com'])
        self.assertEqual(mail.outbox[0].body,
                         'The  number of editors has exceeded the amount of '
                         'users set in your Subscription. Please check it '
                         'out!\nCurrent amount of editors: 2.\nSelected '
                         'amount of editors: 1.')


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
