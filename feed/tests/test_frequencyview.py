from django.test import TestCase
from rest_framework.test import APIRequestFactory

from feed.views import FrequencyViewSet
import factories


class FrequencyListViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        self.frequency = factories.Frequency(
            organization=self.tola_user.organization)

    def test_list_frequency(self):
        request = self.factory.get('')
        request.user = self.tola_user.user
        view = FrequencyViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['frequency'],
                         self.frequency.frequency)
        self.assertEqual(response.data[0]['description'],
                         self.frequency.description)
