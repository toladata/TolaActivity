import datetime
from unittest import skip

from django.test import TestCase, RequestFactory

from TolaActivity.factories import (ProgramFactory, IndicatorFactory, SiteProfileFactory, IndicatorTypeFactory,
                                    LevelFactory, SectorFactory, TolaUserFactory, CollectedDataFactory)
from indicators.views.views_reports import IPTT_ReportView


class FilterPanelTests(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()

    def test_filter_by_program(self):
        """It should only show indicators associated with a given program"""
        user = TolaUserFactory()
        user.countries.add(user.country)
        user.save()
        program = ProgramFactory()
        program.country.add(user.country)
        program.save()
        data = {'program_id': program.id, 'timeframe': 1, 'formprefix': 'filter', 'period': 1}





        request = self.request_factory.post(path='/?program={0}&timeframe=1&period=1'.format(program.id), data=data)

        request.user = user.user
        sectors = SectorFactory.create_batch(3)
        levels = LevelFactory.create_batch(3)
        ind_types = IndicatorTypeFactory.create_batch(3)
        sites = SiteProfileFactory.create_batch(3)
        indicators = IndicatorFactory.create_batch(3)
        min_date_collected = datetime.datetime(2018, 1, 1)
        max_date_collected = datetime.datetime(2018, 2, 2)
        for i in range(len(indicators)):
            indicators[i].program.add(program)
            indicators[i].save()
            if i % 2:
                date = min_date_collected
            else:
                date = max_date_collected
            CollectedDataFactory(indicator=indicators[i], program=program, date_collected=date)

        view = IPTT_ReportView.as_view()(request, **data)
        view.render()
        stuff = str(view)
        for i in range(2):

            self.assertIn(sectors[i].sector, stuff)
            self.assertIn(levels[i].name, stuff)
            self.assertIn(ind_types[i].indicator_type, stuff)
            self.assertIn(sites[i].name, stuff)
            self.assertIn(indicators[i].name, stuff, indicators[i].name)

        self.assertIn(program.name, stuff)

    @skip("Test Not Implemented")
    def test_filter_show_all(self):
        """It should show all indicators for a given project"""
        self.fail("test not implemented")

    @skip("Test Not Implemented")
    def test_filter_limit_by_number(self):
        """
        It should limit the number of indicators shown by a given positive
        int
        """
        self.fail("test not implemented")

    @skip("Test Not Implemented")
    def test_filter_by_date(self):
        """It should show only the indicators that fall in a given date range"""
        self.fail("test not implemented")

    @skip("Test Not Implemented")
    def test_filter_by_level(self):
        """It should show only indicatators of the selected level"""
        self.fail("test not implemented")

    @skip("Test Not Implemented")
    def test_filter_by_type(self):
        """It should only show indicators of the selected type"""
        self.fail("test not implemented")

    @skip("Test Not Implemented")
    def test_filter_by_sector(self):
        """It should only show indicators for the selected sector"""
        self.fail("test not implemented")

    @skip("Test Not Implemented")
    def test_filter_by_site(self):
        """It should only show indicators for the selected site"""
        self.fail("test not implemented")

    @skip("Test Not Implemented")
    def test_filter_by_indicator(self):
        """It should only show the indicators for the selected indicator"""
        self.fail("test not implemented")
