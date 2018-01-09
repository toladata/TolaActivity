from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

import factories
from feed.views import DisaggregationTypeViewSet
from indicators.models import DisaggregationType


class DisaggregationTypeListViewsTest(TestCase):
    def setUp(self):
        factories.Organization(id=0)
        DisaggregationType.objects.bulk_create([
            DisaggregationType(disaggregation_type='DisaggregationType1'),
            DisaggregationType(disaggregation_type='DisaggregationType2'),
        ])

        factory = APIRequestFactory()
        self.request_get = factory.get('/api/disaggregationtype/')

    def test_list_disaggregationtype_superuser(self):
        self.request_get.user = factories.User.build(is_superuser=True,
                                                     is_staff=True)
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
        DisaggregationType.objects.create(
            disaggregation_type='DisaggregationType0',
            organization=tola_user.organization)

        self.request_get.user = tola_user.user
        view = DisaggregationTypeViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class DisaggregationTypeCreateViewsTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()
        self.factory = APIRequestFactory()

    def test_create_disaggregationtype_normaluser_missing_values(self):
        data = {}
        request = self.factory.post('', data)
        request.user = self.tola_user.user
        view = DisaggregationTypeViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 400)

    def test_create_disaggregationtype_normaluser(self):
        organization_url = reverse(
            'organization-detail',
            kwargs={'pk': self.tola_user.organization.pk})
        data = {
            'disaggregation_type': 'Some Type',
            'description': 'Some Desc',
        }
        request = self.factory.post('', data)
        request.user = self.tola_user.user
        view = DisaggregationTypeViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['disaggregation_type'], u'Some Type')
        self.assertEqual(response.data['description'], u'Some Desc')
        self.assertIn(organization_url, response.data['organization'])

        disaggregation_type = DisaggregationType.objects.get(
            pk=response.data['id'])
        self.assertEqual(disaggregation_type.disaggregation_type, u'Some Type')
        self.assertEqual(disaggregation_type.description, u'Some Desc')
        self.assertEqual(disaggregation_type.organization,
                         self.tola_user.organization)
