import mock
from django.test import TestCase

from factories.indicators_models import ExternalServiceFactory
from indicators.views.views_indicators import import_indicator


class ImportIndicatorTests(TestCase):

    @mock.patch("indicators.views.views_indicators.requests.get")
    def test_remote_resource_true(self, mock_get):
        """
        It should deserialize the response content if deserialize is left
        true by default
        """
        class mock_response(object):
            content = '{"hello": 1}'

        mock_get.return_value = mock_response()
        service = ExternalServiceFactory(name="Import Ind Test Service")
        result = import_indicator(service=service.id)

        self.assertDictEqual(result, {'hello': 1})

    @mock.patch("indicators.views.views_indicators.requests.get")
    def test_remote_resource_false(self, mock_get):
        """
        It should return the response object if deserialize is set to anything
        other than bool True
        """

        class mock_response(object):
            content = '{"hello": 1}'

        mock_get.return_value = mock_response()
        service = ExternalServiceFactory(name="Import Ind Test Service")
        result = import_indicator(service=service.id, deserialize='')
        self.assertIsInstance(result, mock_response)


