from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.db import IntegrityError
from django.test import TestCase

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
        WorkflowLevel1.objects.get(name='Financial Assistance and Building '
                                   'Resilience in Conflict Areas')

    def test_load_demo_data_two_times_crashes_but_db_keeps_consistent(self):
        args = ['--demo']
        opts = {}
        call_command('loadinitialdata', *args, **opts)

        User.objects.all().delete()

        with self.assertRaises(IntegrityError):
            call_command('loadinitialdata', *args, **opts)

        self.assertRaises(User.DoesNotExist, User.objects.get,
                          first_name="Andrew", last_name="Ham")
