from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.db import IntegrityError, connection
from django.test import TestCase

from indicators.models import IndicatorType
from tola.management.commands.loadinitialdata import (
    DEFAULT_WORKFLOWLEVEL1_ID, DEFAULT_WORKFLOWLEVEL1_NAME)
from workflow.models import (Country, Organization, Sector, ROLE_VIEW_ONLY,
                             ROLE_ORGANIZATION_ADMIN, ROLE_PROGRAM_ADMIN,
                             ROLE_PROGRAM_TEAM, WorkflowLevel1)


class LoadInitialDataTest(TestCase):
    def test_load_basic_data(self):
        args = []
        opts = {}
        call_command('loadinitialdata', *args, **opts)

        Organization.objects.get(name="TolaData")
        for name in (ROLE_VIEW_ONLY, ROLE_ORGANIZATION_ADMIN, ROLE_PROGRAM_ADMIN,
                     ROLE_PROGRAM_TEAM):
            Group.objects.get(name=name)
        Country.objects.get(code="AF")
        Sector.objects.get(sector="Agriculture")
        for name in ("Custom", "Donor", "Standard"):
            IndicatorType.objects.get(indicator_type=name)

    def test_load_basic_data_two_times_no_crash(self):
        args = []
        opts = {}
        call_command('loadinitialdata', *args, **opts)
        call_command('loadinitialdata', *args, **opts)

        # We make sure it only returns one unique object of each model
        Organization.objects.get(name="TolaData")
        for name in (ROLE_VIEW_ONLY, ROLE_ORGANIZATION_ADMIN, ROLE_PROGRAM_ADMIN,
                     ROLE_PROGRAM_TEAM):
            Group.objects.get(name=name)
        Country.objects.get(code="AF")
        Sector.objects.get(sector="Agriculture")

    def test_load_demo_data(self):
        args = ['--demo']
        opts = {}
        call_command('loadinitialdata', *args, **opts)

        Organization.objects.get(name="TolaData")
        for name in (ROLE_VIEW_ONLY, ROLE_ORGANIZATION_ADMIN, ROLE_PROGRAM_ADMIN,
                     ROLE_PROGRAM_TEAM):
            Group.objects.get(name=name)
        Country.objects.get(code="AF")
        Sector.objects.get(sector="Agriculture")
        User.objects.get(first_name="Andrew", last_name="Ham")
        WorkflowLevel1.objects.get(id=DEFAULT_WORKFLOWLEVEL1_ID,
                                   name=DEFAULT_WORKFLOWLEVEL1_NAME)

    def test_load_demo_data_check_indices_reset(self):
        args = ['--demo']
        opts = {}
        call_command('loadinitialdata', *args, **opts)

        cursor = connection.cursor()
        cursor.execute("SELECT nextval('workflow_country_id_seq')")
        self.assertNotEqual(int(cursor.fetchone()[0]), 1)

        cursor.execute("SELECT nextval('workflow_workflowteam_id_seq')")
        self.assertNotEqual(int(cursor.fetchone()[0]), 1)

    def test_load_demo_data_two_times_crashes_but_db_keeps_consistent(self):
        args = ['--demo']
        opts = {}
        call_command('loadinitialdata', *args, **opts)

        User.objects.all().delete()

        with self.assertRaises(IntegrityError):
            call_command('loadinitialdata', *args, **opts)

        self.assertRaises(User.DoesNotExist, User.objects.get,
                          first_name="Andrew", last_name="Ham")
