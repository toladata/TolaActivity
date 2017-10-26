from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import OrganizationViewSet
from workflow.models import Organization


class OrganizationViewTest(TestCase):
    def setUp(self):
        factories.Organization.create_batch(2)

        factory = APIRequestFactory()
        self.request = factory.get('/api/organization/')

    def test_list_organization_superuser(self):
        self.request.user = factories.User.build(is_superuser=True, is_staff=True)
        view = OrganizationViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_organization_normaluser_one_result(self):
        tola_user = factories.TolaUser()
        self.request.user = tola_user.user
        view = OrganizationViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
