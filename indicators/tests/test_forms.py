from django.test import TestCase

from TolaActivity.factories import (IndicatorTypeFactory, IndicatorFactory, LevelFactory, SiteProfileFactory,
                                    SectorFactory)
from indicators.forms import IPTTReportFilterForm


class TestFilterForm(TestCase):

    def test_new_unbound_form(self):
        form = IPTTReportFilterForm()

        self.assertIsInstance(form, IPTTReportFilterForm)

    def test_form_populates(self):
        """The form should populate several fields from the db"""

        sectors = SectorFactory.create_batch(3)
        levels = LevelFactory.create_batch(3)
        ind_types = IndicatorTypeFactory.create_batch(3)
        sites = SiteProfileFactory.create_batch(3)
        indicators = IndicatorFactory.create_batch(3)

        form = IPTTReportFilterForm()

        stuff = str(form)
        for i in range(2):
            self.assertIn(sectors[i].sector, stuff)
            self.assertIn(levels[i].name, stuff)
            self.assertIn(ind_types[i].indicator_type, stuff)
            self.assertIn(sites[i].name, stuff)
            self.assertIn(indicators[i].name, stuff)



