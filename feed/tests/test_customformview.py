from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import factories
from feed.views import CustomFormViewSet


class CustomFormViewTest(TestCase):
    def setUp(self):
        self.user = factories.User(is_superuser=True, is_staff=True)
        self.organization = factories.Organization(id=1)
        factories.TolaUser(user=self.user, organization=self.organization)
        factory = APIRequestFactory()
        self.request = factory.post('/api/customform/')

    def test_create_customform(self):
        user_url = reverse('user-detail', kwargs={'pk': self.user.id},
                           request=self.request)

        data = {'name': '4W Daily Activity Report'}
        self.request = APIRequestFactory().post('/api/customform/', data)
        self.request.user = self.user
        view = CustomFormViewSet.as_view({'post': 'create'})
        response = view(self.request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'4W Daily Activity Report')
        self.assertEqual(response.data['owner'], user_url)
