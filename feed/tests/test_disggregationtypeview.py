from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import DisaggregationTypeViewSet
from indicators.models import DisaggregationType
from workflow.models import Organization


class DisaggregationTypeViewsTest(TestCase):
    def setUp(self):
        factories.Organization(id=0)
        DisaggregationType.objects.bulk_create([
            DisaggregationType(disaggregation_type='DisaggregationType1'),
            DisaggregationType(disaggregation_type='DisaggregationType2'),
        ])

        factory = APIRequestFactory()
        self.request_get = factory.get('/api/disaggregationtype/')
        self.request_post = factory.post('/api/disaggregationtype/')

    def test_list_disaggregationtype_superuser(self):
        self.request_get.user = factories.User.build(is_superuser=True, is_staff=True)
        view = DisaggregationTypeViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_disaggregationtype_normaluser(self):
        tola_user = factories.TolaUser()
        self.request_get.user = tola_user.user
        view = DisaggregationTypeViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_disaggregationtype_normaluser_one_result(self):
        tola_user = factories.TolaUser()
        DisaggregationType.objects.create(disaggregation_type='DisaggregationType0',
                                          organization=tola_user.organization)

        self.request_get.user = tola_user.user
        view = DisaggregationTypeViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
