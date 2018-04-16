from django.test import TestCase

from indicators.forms import IPTTReportFilterForm


class TestFilterForm(TestCase):

    def test_new_unbound_form(self):
        form = IPTTReportFilterForm()

        self.assertIsInstance(form, IPTTReportFilterForm)
