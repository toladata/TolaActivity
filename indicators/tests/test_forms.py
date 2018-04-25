from django.test import TestCase, RequestFactory
from TolaActivity.factories import (
    IndicatorTypeFactory, IndicatorFactory, LevelFactory, SiteProfileFactory,
    SectorFactory, ProgramFactory, CollectedDataFactory, UserFactory
)
from indicators.forms import IPTTReportFilterForm


class TestFilterForm(TestCase):

    def test_form_populates(self):
        """The form should populate several fields from the db"""
        request = RequestFactory().post('/')
        request.user = UserFactory()
        sectors = SectorFactory.create_batch(3)
        levels = LevelFactory.create_batch(3)
        ind_types = IndicatorTypeFactory.create_batch(3)

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
        form = IPTTReportFilterForm(*[request], **{'program':p})

        stuff = str(form)
        self.assertIn(expected.name, stuff)
        self.assertIn(expected2.name, stuff)
        self.assertIn(indicator.name, stuff)
        for i in range(2):
            self.assertIn(sectors[i].sector, stuff)
            self.assertIn(levels[i].name, stuff)
            self.assertIn(ind_types[i].indicator_type, stuff)



