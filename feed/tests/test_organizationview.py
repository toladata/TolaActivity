from django.test import TestCase
from rest_framework.test import APIRequestFactory

from feed.views import OrganizationViewSet
import factories
from workflow.models import Organization, TolaUser


class OrganizationViewTest(TestCase):
    def setUp(self):
        Organization.objects.bulk_create([
            Organization(name='Organization_0'),
            Organization(name='Organization_1'),
        ])

        factory = APIRequestFactory()
        self.request = factory.get('/api/organization/')

    def test_list_organization_superuser(self):
        self.request.user = factories.User.build(is_superuser=True, is_staff=True)
        view = OrganizationViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_organization_normaluser_one_result(self):
        user = factories.User()
        organization = Organization.objects.create(name="TestOrg")
        TolaUser.objects.create(user=user, organization=organization)

        self.request.user = user
        view = OrganizationViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
