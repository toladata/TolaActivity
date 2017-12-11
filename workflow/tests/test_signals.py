import os

from django.test import TestCase

import factories
from tola import DEMO_BRANCH
from tola.management.commands.loadinitialdata import (
    DEFAULT_WORKFLOWLEVEL1_ID, DEFAULT_WORKFLOWLEVEL1_NAME)
from workflow.models import WorkflowTeam, ROLE_VIEW_ONLY


class AddUsersToDefaultWorkflowLevel1Test(TestCase):
    def test_not_demo_env(self):
        factories.TolaUser()  # triggers the signal
        self.assertEqual(WorkflowTeam.objects.all().count(), 0)

    def test_demo_env_no_wflvl1_matching(self):
        os.environ['APP_BRANCH'] = DEMO_BRANCH
        factories.WorkflowLevel1(name=DEFAULT_WORKFLOWLEVEL1_NAME)
        factories.TolaUser()  # triggers the signal
        self.assertEqual(WorkflowTeam.objects.all().count(), 0)

        factories.WorkflowLevel1(id=DEFAULT_WORKFLOWLEVEL1_ID, name='Any')
        factories.TolaUser(
            user=factories.User(first_name='Ringo', last_name='Starr')
        )  # triggers the signal
        self.assertEqual(WorkflowTeam.objects.all().count(), 0)
        os.environ['APP_BRANCH'] = ''

    def test_demo_workflowteam_assignment(self):
        os.environ['APP_BRANCH'] = DEMO_BRANCH
        role = factories.Group(name=ROLE_VIEW_ONLY)
        wflvl1 = factories.WorkflowLevel1(id=DEFAULT_WORKFLOWLEVEL1_ID,
                                          name=DEFAULT_WORKFLOWLEVEL1_NAME)

        tola_user = factories.TolaUser(
            user=factories.User(first_name='Ringo', last_name='Starr')
        )  # triggers the signal
        WorkflowTeam.objects.get(
            workflow_user=tola_user, role=role, workflowlevel1=wflvl1)
        os.environ['APP_BRANCH'] = ''

    def test_demo_workflowteam_assignment_not_reassigned_on_update(self):
        os.environ['APP_BRANCH'] = DEMO_BRANCH
        role = factories.Group(name=ROLE_VIEW_ONLY)
        wflvl1 = factories.WorkflowLevel1(id=DEFAULT_WORKFLOWLEVEL1_ID,
                                          name=DEFAULT_WORKFLOWLEVEL1_NAME)

        tola_user = factories.TolaUser(
            user=factories.User(first_name='Ringo', last_name='Starr')
        )  # triggers the signal
        tola_user.name = 'Laura Pausini'
        tola_user.save()

        num_results = WorkflowTeam.objects.filter(
            workflow_user=tola_user, role=role, workflowlevel1=wflvl1).count()
        self.assertEqual(num_results, 1)
        os.environ['APP_BRANCH'] = ''
