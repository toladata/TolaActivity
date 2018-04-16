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

        SectorFactory.create_batch(3)
        LevelFactory.create_batch(3)
        IndicatorTypeFactory.create_batch(3)
        SiteProfileFactory.create_batch(3)
        IndicatorFactory.create_batch(3)

        form = IPTTReportFilterForm()
        print form
