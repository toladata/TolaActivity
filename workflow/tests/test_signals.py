import logging
import os

from chargebee import APIError
from chargebee.models import Subscription
from django.core import mail
from django.test import TestCase, override_settings, tag
from django.db.models import Sum
from mock import Mock, patch

import factories
from tola import DEMO_BRANCH
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

    @override_settings(DEFAULT_REPLY_TO='noreply@example.com')
    @override_settings(SALES_TEAM_EMAIL='sales@example.com')
    @override_settings(PAYMENT_PORTAL_URL='example.com')
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
        self.assertIn('Edit user exceeding notification',
                      mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].to, [self.tola_user.user.email])
        self.assertEqual(mail.outbox[0].reply_to, ['noreply@example.com'])
        self.assertEqual(mail.outbox[0].bcc, ['sales@example.com'])

        # Text body
        org_admin_name = 'Hi {},'.format(self.tola_user.name)
        self.assertIn(org_admin_name, mail.outbox[0].body)

        available_seats = 'Purchased user seats: 1'
        self.assertIn(available_seats, mail.outbox[0].body)

        used_seats = 'Current edit users in the system: 2'
        self.assertIn(used_seats, mail.outbox[0].body)

        payment_portal_url = 'example.com'
        self.assertIn(payment_portal_url, mail.outbox[0].body)

        # HTML body
        org_admin_name = '<br>Hi {},</span>'.format(self.tola_user.name)
        self.assertIn(org_admin_name, mail.outbox[0].alternatives[0][0])

        available_seats = 'Purchased user seats: <b>1</b>'
        self.assertIn(available_seats, mail.outbox[0].alternatives[0][0])

        used_seats = 'Current edit users in the system: <b>2</b>'
        self.assertIn(used_seats, mail.outbox[0].alternatives[0][0])

        payment_portal_url = '<a href="example.com" target="_blank">Payment ' \
                             'portal</a>'
        self.assertIn(payment_portal_url, mail.outbox[0].alternatives[0][0])

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

    @override_settings(DEFAULT_REPLY_TO='noreply@example.com')
    @override_settings(SALES_TEAM_EMAIL='sales@example.com')
    @override_settings(PAYMENT_PORTAL_URL='example.com')
    def test_exceeded_seats_not_notify_when_role_changed(self):
        """ If user is org admin and program admin and users orgadmin
         role removed then org admin should not get notification because
          user still has seat as program admin."""
        external_response = self.ExternalResponse(None)
        Subscription.retrieve = Mock(return_value=external_response)
        self.tola_user.user.groups.add(self.group_org_admin)
        self.tola_user.user.save()
        self.org = Organization.objects.get(pk=self.org.id)

        user = factories.User(first_name='John', last_name='Lennon')
        tolauser = factories.TolaUser(user=user, organization=self.org)
        tolauser.user.save()
        wflvl1_1 = factories.WorkflowLevel1(name='WorkflowLevel1_1')
        wfl_team = factories.WorkflowTeam(workflow_user=tolauser,
                                          workflowlevel1=wflvl1_1,
                                          role=self.group_program_team)

        # It should notify the OrgAdmin
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 2)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Edit user exceeding notification',
                      mail.outbox[0].subject)

        # after role changed it should not notify
        wfl_team.role = self.group_program_admin
        wfl_team.save()

        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 2)
        self.assertEqual(len(mail.outbox), 1)

    @override_settings(DEFAULT_REPLY_TO='noreply@example.com')
    @override_settings(SALES_TEAM_EMAIL='sales@example.com')
    @override_settings(PAYMENT_PORTAL_URL='example.com')
    def test_exceeded_seats_not_notify_when_role_removed(self):
        """ If user is org admin and program admin and users orgadmin
         role removed then org admin should not get notification because
          user still has seat as program admin."""
        external_response = self.ExternalResponse(None)
        Subscription.retrieve = Mock(return_value=external_response)
        self.tola_user.user.groups.add(self.group_org_admin)
        self.tola_user.user.save()
        self.org = Organization.objects.get(pk=self.org.id)

        user = factories.User(first_name='John', last_name='Lennon')
        tolauser = factories.TolaUser(user=user, organization=self.org)
        tolauser.user.save()
        wflvl1_1 = factories.WorkflowLevel1(name='WorkflowLevel1_1')
        wfl_team = factories.WorkflowTeam(workflow_user=tolauser,
                                          workflowlevel1=wflvl1_1,
                                          role=self.group_program_team)

        # It should notify the OrgAdmin
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 2)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Edit user exceeding notification',
                      mail.outbox[0].subject)

        # after role changed it should not notify
        wfl_team.role = self.group_view_only
        wfl_team.save()

        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 1)
        self.assertEqual(len(mail.outbox), 1)


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

    @override_settings(DEFAULT_REPLY_TO='noreply@example.com')
    @override_settings(SALES_TEAM_EMAIL='sales@example.com')
    @override_settings(PAYMENT_PORTAL_URL='example.com')
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
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn('Edit user exceeding notification',
                      mail.outbox[0].subject)

        for outbox in mail.outbox:
            self.assertEqual(outbox.reply_to, ['noreply@example.com'])
            self.assertEqual(outbox.bcc, ['sales@example.com'])
            self.assertIn(outbox.to[0], [self.tola_user.user.email,
                                         user.email])

            # Text body
            org_admin_name = ''
            if outbox.to[0] == self.tola_user.user.email:
                org_admin_name = 'Hi {},'.format(self.tola_user.name)
            elif outbox.to[0] == user.email:
                org_admin_name = 'Hi {},'.format(tolauser.name)

            self.assertIn(org_admin_name, outbox.body)

            available_seats = 'Purchased user seats: 1'
            self.assertIn(available_seats, outbox.body)

            used_seats = 'Current edit users in the system: 2'
            self.assertIn(used_seats, outbox.body)

            payment_portal_url = 'example.com'
            self.assertIn(payment_portal_url, outbox.body)

            # HTML body
            org_admin_name = ''
            if outbox.to[0] == self.tola_user.user.email:
                org_admin_name = '<br>Hi {},</span>'.format(self.tola_user.name)
            elif outbox.to[0] == user.email:
                org_admin_name = '<br>Hi {},</span>'.format(tolauser.name)

            self.assertIn(org_admin_name, outbox.alternatives[0][0])

            available_seats = 'Purchased user seats: <b>1</b>'
            self.assertIn(available_seats, outbox.alternatives[0][0])

            used_seats = 'Current edit users in the system: <b>2</b>'
            self.assertIn(used_seats, outbox.alternatives[0][0])

            payment_portal_url = '<a href="example.com" target="_blank">' \
                                 'Payment portal</a>'
            self.assertIn(payment_portal_url, outbox.alternatives[0][0])

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

    @override_settings(DEFAULT_REPLY_TO='noreply@example.com')
    @override_settings(SALES_TEAM_EMAIL='sales@example.com')
    @override_settings(PAYMENT_PORTAL_URL='example.com')
    def test_exceeded_seats_not_notify_when_role_removed(self):
        """ If user has already seat as an orgadmin and when its role removed
         than org admin should not get notification email """
        external_response = self.ExternalResponse(None)
        Subscription.retrieve = Mock(return_value=external_response)

        self.tola_user.user.groups.add(self.group_org_admin)
        self.tola_user.user.save()
        self.org = Organization.objects.get(pk=self.org.id)
        self.assertEqual(self.org.chargebee_used_seats, 1)
        self.assertEqual(len(mail.outbox), 0)

        user = factories.User(first_name='John', last_name='Lennon')
        tolauser = factories.TolaUser(user=user, organization=self.org)
        tolauser.user.groups.add(self.group_org_admin)
        tolauser.user.save()
        self.org = Organization.objects.get(pk=self.org.id)

        self.assertEqual(self.org.chargebee_used_seats, 2)
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn('Edit user exceeding notification',
                      mail.outbox[0].subject)

        user2 = factories.User(first_name='Leonard', last_name='Cohen')
        tolauser2 = factories.TolaUser(user=user2, organization=self.org)
        tolauser2.user.groups.add(self.group_org_admin)
        tolauser2.user.save()

        self.org = Organization.objects.get(pk=self.org.id)
        self.assertEqual(self.org.chargebee_used_seats, 3)
        self.assertEqual(len(mail.outbox), 5)

        # org admin removed but mail outbox still should be same
        tolauser2.user.groups.remove(self.group_org_admin)

        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 2)
        self.assertEqual(len(mail.outbox), 5)

    @override_settings(DEFAULT_REPLY_TO='noreply@example.com')
    @override_settings(SALES_TEAM_EMAIL='sales@example.com')
    @override_settings(PAYMENT_PORTAL_URL='example.com')
    def test_exceeded_seats_not_notify_when_one_of_multiple_role_removed(self):
        """ If user is org admin and program admin at the same time and users
         orgadmin role removed then org admin should not get notification
          because user still has seat as program admin."""
        external_response = self.ExternalResponse(None)
        Subscription.retrieve = Mock(return_value=external_response)
        self.tola_user.user.groups.add(self.group_org_admin)
        self.tola_user.user.save()
        user = factories.User(first_name='John', last_name='Lennon')

        self.org = Organization.objects.get(pk=self.org.id)

        tolauser = factories.TolaUser(user=user, organization=self.org)
        tolauser.user.groups.add(self.group_org_admin)
        tolauser.user.save()
        wflvl1_1 = factories.WorkflowLevel1(name='WorkflowLevel1_1')
        factories.WorkflowTeam(workflow_user=tolauser,
                               workflowlevel1=wflvl1_1,
                               role=self.group_program_admin)

        # It should notify the OrgAdmin
        organization = Organization.objects.get(pk=self.org.id)
        self.assertEqual(organization.chargebee_used_seats, 2)
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn('Edit user exceeding notification',
                      mail.outbox[0].subject)

        tolauser.user.groups.remove(self.group_org_admin)
        self.assertEqual(organization.chargebee_used_seats, 2)
        self.assertEqual(len(mail.outbox), 2)


@tag('pkg')
class AddPublicUrlTokenTest(TestCase):
    def test_add_public_url_token_create_not_public_url(self):
        dashboard = factories.Dashboard()
        self.assertNotEqual(dashboard.public, Dashboard.PUBLIC_URL)
        self.assertIsNone(dashboard.public_url_token)

    def test_add_public_url_token_create_public_url(self):
        dashboard = factories.Dashboard(public=Dashboard.PUBLIC_URL)
        self.assertEqual(dashboard.public, Dashboard.PUBLIC_URL)
        self.assertIsNotNone(dashboard.public_url_token)

    def test_add_public_url_token_update_not_public_url(self):
        dashboard = factories.Dashboard()
        dashboard.public = Dashboard.PUBLIC_ALL
        dashboard.save()

        self.assertEqual(dashboard.public, Dashboard.PUBLIC_ALL)
        self.assertIsNone(dashboard.public_url_token)

    def test_add_public_url_token_update_public_url(self):
        dashboard = factories.Dashboard()
        dashboard.public = Dashboard.PUBLIC_URL
        dashboard.save()

        self.assertEqual(dashboard.public, Dashboard.PUBLIC_URL)
        self.assertIsNotNone(dashboard.public_url_token)

    def test_add_public_url_token_create_and_update(self):
        dashboard = factories.Dashboard(public=Dashboard.PUBLIC_URL)
        self.assertEqual(dashboard.public, Dashboard.PUBLIC_URL)
        self.assertIsNotNone(dashboard.public_url_token)

        dashboard.public = Dashboard.PUBLIC_ALL
        dashboard.save()
        self.assertEqual(dashboard.public, Dashboard.PUBLIC_ALL)
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
class BudgetUpdateTest(TestCase):
    def setUp(self):
        self.organization = factories.Organization()
        self.user = factories.User()
        self.tola_user = factories.TolaUser(organization=self.organization)

    def test_delete_budget_value_from_wfl2(self):
        '''When budget deleted, then related wfl2s total_estimated_budget
        should be updated'''

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
