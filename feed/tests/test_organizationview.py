from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from feed.views import OrganizationViewSet
from workflow.models import Organization, TolaUser


class OrganizationViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        Organization.objects.bulk_create([
            Organization(name='Organization_0'),
            Organization(name='Organization_1'),
        ])

        factory = APIRequestFactory()
        self.request = factory.get('/api/organization/')

    def test_list_organization_superuser(self):
        self.request.user = self.user
        view = OrganizationViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_organization_normaluser_one_result(self):
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save()
        organization = Organization.objects.create(name="TestOrg")
        TolaUser.objects.create(user=self.user, organization=organization)

        self.request.user = self.user
        view = OrganizationViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
