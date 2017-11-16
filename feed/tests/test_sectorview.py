from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import json
import factories
from feed.views import SectorViewSet


class SectorViewTest(TestCase):
    def setUp(self):
        self.user = factories.User(is_superuser=True, is_staff=True)
        self.organization = factories.Organization(id=1)
        factories.TolaUser(user=self.user, organization=self.organization)
        factory = APIRequestFactory()
        self.request = factory.post('/api/sector/')

    def test_create_sector(self):
        user_url = reverse('user-detail', kwargs={'pk': self.user.id},
                           request=self.request)

        data = {'sector': 'Agriculture'}
        self.request = APIRequestFactory().post('/api/sector/', data)
        self.request.user = self.user
        view = SectorViewSet.as_view({'post': 'create'})
        response = view(self.request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['sector'], u'Agriculture')
        self.assertEqual(response.data['created_by'], user_url)

    def test_create_sector_json(self):
        user_url = reverse('user-detail', kwargs={'pk': self.user.id},
                           request=self.request)

        data = {'sector': 'Agriculture'}
        self.request = APIRequestFactory().post(
            '/api/sector/', json.dumps(data), content_type='application/json')
        self.request.user = self.user
        view = SectorViewSet.as_view({'post': 'create'})
        response = view(self.request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['sector'], u'Agriculture')
        self.assertEqual(response.data['created_by'], user_url)
