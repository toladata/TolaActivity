import logging
import sys

from django.contrib.auth.models import Group, User
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.db import IntegrityError, connection
from django.test import TestCase, override_settings, tag

import factories
from indicators.models import (Level, Frequency, Indicator, PeriodicTarget,
                               CollectedData, IndicatorType)
from tola.management.commands.loadinitialdata import (
    Command, DEFAULT_WORKFLOW_LEVEL_1S, DEFAULT_ORG, DEFAULT_COUNTRY_CODES)
from workflow.models import (Country, Organization, Sector, ROLE_VIEW_ONLY,
                             ROLE_ORGANIZATION_ADMIN, ROLE_PROGRAM_ADMIN,
                             ROLE_PROGRAM_TEAM, WorkflowLevel1, TolaUser, Group,
                             Sector, Stakeholder, Milestone, WorkflowLevel1,
                             WorkflowLevel2, WorkflowLevel1Sector, WorkflowTeam,
                             SiteProfile)


class DevNull(object):
    def write(self, data):
        pass


@tag('pkg')
class LoadInitialDataTest(TestCase):
    def setUp(self):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        sys.stdout = DevNull()
        sys.stderr = DevNull()
        logging.disable(logging.ERROR)

    def tearDown(self):
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr
        logging.disable(logging.NOTSET)

    @override_settings(DEFAULT_ORG='')
    def test_without_default_organization_conf_var(self):
        args = []
        opts = {}
        with self.assertRaises(ImproperlyConfigured):
            call_command('loadinitialdata', *args, **opts)


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
        WorkflowLevel1.objects.get(id=DEFAULT_WORKFLOW_LEVEL_1S[0][0],
                                   name=DEFAULT_WORKFLOW_LEVEL_1S[0][1])

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

    def test_clear_database_without_default_org(self):
        command = Command()
        with self.assertRaises(IntegrityError):
            command._clear_database()

    def test_clear_database_without_default_countries(self):
        Organization.objects.create(**DEFAULT_ORG)
        command = Command()
        with self.assertRaises(IntegrityError):
            command._clear_database()

    def test_clear_database_clears_stuff(self):
        organization = Organization.objects.create(**DEFAULT_ORG)
        country = Country.objects.create(code=DEFAULT_COUNTRY_CODES[0])
        Country.objects.create(code=DEFAULT_COUNTRY_CODES[1])

        factories.TolaUser(
            organization=Organization.objects.create(name='Org To Delete'),
            country=Country.objects.create(code='RM'),
            name='Kurt Cobain')

        command = Command()
        command._clear_database()

        tolauser = TolaUser.objects.get(name='Kurt Cobain')
        self.assertEqual(tolauser.organization, organization)
        self.assertEqual(tolauser.country, country)
        organizations = Organization.objects.all()
        self.assertEqual(organizations[0], organization)
        self.assertEqual(len(organizations), 1)
        self.assertTrue(
            Country.objects.filter(code__in=DEFAULT_COUNTRY_CODES).exists())
        self.assertEqual(Country.objects.all().count(), 2)
        self.assertEqual(Group.objects.all().count(), 0)
        self.assertEqual(Sector.objects.all().count(), 0)
        self.assertEqual(Stakeholder.objects.all().count(), 0)
        self.assertEqual(Milestone.objects.all().count(), 0)
        self.assertEqual(WorkflowLevel1.objects.all().count(), 0)
        self.assertEqual(WorkflowLevel2.objects.all().count(), 0)
        self.assertEqual(Level.objects.all().count(), 0)
        self.assertEqual(Frequency.objects.all().count(), 0)
        self.assertEqual(Indicator.objects.all().count(), 0)
        self.assertEqual(PeriodicTarget.objects.all().count(), 0)
        self.assertEqual(CollectedData.objects.all().count(), 0)
        self.assertEqual(WorkflowLevel1Sector.objects.all().count(), 0)
        self.assertEqual(WorkflowTeam.objects.all().count(), 0)

    def test_load_basic_data_and_restore_does_not_crash(self):
        args = []
        opts = {}
        call_command('loadinitialdata', *args, **opts)

        args = ['--restore']
        opts = {}
        call_command('loadinitialdata', *args, **opts)

    def test_load_demo_data_and_restore_does_not_crash(self):
        args = []
        opts = {}
        call_command('loadinitialdata', *args, **opts)
        # Just to double check sequences later
        factories.WorkflowLevel1.create_batch(20)
        # To check assignments to this user
        tola_user = factories.TolaUser(
            organization=Organization.objects.create(name='Org To Delete'),
            country=Country.objects.create(code='RM'),
            name='Kurt Cobain')

        args = ['--restore']
        opts = {}
        call_command('loadinitialdata', *args, **opts)

        # We check that we don't have repeated data and that sequences are
        # reset.
        WorkflowLevel1.objects.get(id=DEFAULT_WORKFLOW_LEVEL_1S[0][0],
                                   name=DEFAULT_WORKFLOW_LEVEL_1S[0][1])
        WorkflowLevel1.objects.get(id=DEFAULT_WORKFLOW_LEVEL_1S[1][0],
                                   name=DEFAULT_WORKFLOW_LEVEL_1S[1][1])
        expected_next = WorkflowLevel1.objects.all().count() + 1
        wflvl1_next = factories.WorkflowLevel1()
        self.assertEqual(wflvl1_next.id, expected_next)

        wflvl1s = [
            id for id in WorkflowTeam.objects.\
                values_list('workflowlevel1_id', flat=True).\
                filter(workflow_user=tola_user)
        ]
        self.assertEqual(sorted(wflvl1s), [3, 6])

    def test_restore_twice_does_not_crash(self):
        args = []
        opts = {}
        call_command('loadinitialdata', *args, **opts)

        args = ['--restore']
        opts = {}
        call_command('loadinitialdata', *args, **opts)
        call_command('loadinitialdata', *args, **opts)

    def test_restore_having_historical_dependent_data(self):
        organization = factories.Organization(name='Some org')
        country = factories.Country(country='Brazil', code='BR')
        factories.SiteProfile(organization=organization, country=country)
        siteprofile_history_id = SiteProfile.history.get(organization=organization).id

        args = ['--demo']
        opts = {}
        call_command('loadinitialdata', *args, **opts)

        args = ['--restore']
        opts = {}
        call_command('loadinitialdata', *args, **opts)
        self.assertRaises(SiteProfile.history.model.DoesNotExist,
                          SiteProfile.history.get, id=siteprofile_history_id)
