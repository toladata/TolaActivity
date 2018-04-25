from django.test import TestCase

from TolaActivity.factories import (ProgramFactory, IndicatorFactory, CollectedDataFactory, SiteProfileFactory)
from workflow.models import SiteProfile


class TestProgramMethods(TestCase):

    def test_get_sites(self):
        """It should return all and only the sites for a given program"""



        p = ProgramFactory()
        indicator = IndicatorFactory(program=p)
        IndicatorFactory.create_batch(3)
        collected_data = CollectedDataFactory(indicator=indicator)
        CollectedDataFactory.create_batch(3)
        expected = SiteProfileFactory()
        expected2 = SiteProfileFactory()
        collected_data.site.add(expected2)
        collected_data.site.add(expected)
        SiteProfileFactory.create_batch(3)
        sites = p.get_sites()

        self.assertEqual(len(sites), 2)
        self.assertTrue(len(SiteProfile.objects.all()), 5)
