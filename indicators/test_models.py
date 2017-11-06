from django.test import TestCase

from indicators.models import Level
from workflow.models import WorkflowLevel1, Organization


class LevelModelTest(TestCase):
    def test_save_level_org_same_as_wflvl1(self):
        self.wflvl1 = WorkflowLevel1.objects.create(name='WorkflowLevel1')
        self.organization = Organization.objects.create(name='Org')
        org = Organization.objects.first()
        self.wflvl1.organization = self.organization
        self.wflvl1.save()
        level = Level.objects.create(name='TestIndicator', workflowlevel1=self.wflvl1)
        level.save()
        self.assertEqual(level.organization, self.organization)
