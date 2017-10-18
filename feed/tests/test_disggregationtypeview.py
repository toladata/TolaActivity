from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from feed.views import DisaggregationTypeViewSet
from indicators.models import DisaggregationType
from workflow.models import Organization, TolaUser


class DisaggregationTypeViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        Organization.objects.create(id=0, name="DefaultOrg")
        DisaggregationType.objects.bulk_create([
            DisaggregationType(disaggregation_type='DisaggregationType1'),
            DisaggregationType(disaggregation_type='DisaggregationType2'),
        ])

        factory = APIRequestFactory()
        self.request_get = factory.get('/api/disaggregationtype/')
        self.request_post = factory.post('/api/disaggregationtype/')

    def test_list_disaggregationtype_superuser(self):
        self.request_get.user = self.user
        view = DisaggregationTypeViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_disaggregationtype_normaluser(self):
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save()
        organization = Organization.objects.create(name="TestOrg")
        TolaUser.objects.create(user=self.user, organization=organization)

        self.request_get.user = self.user
        view = DisaggregationTypeViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_disaggregationtype_normaluser_one_result(self):
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save()
        organization = Organization.objects.create(name="TestOrg")
        TolaUser.objects.create(user=self.user, organization=organization)

        DisaggregationType.objects.create(disaggregation_type='DisaggregationType0', organization=organization)

        self.request_get.user = self.user
        view = DisaggregationTypeViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
