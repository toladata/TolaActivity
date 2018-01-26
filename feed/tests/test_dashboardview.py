import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import factories
from feed.views import DashboardViewSet


class DashboardListViewTest(TestCase):
    def setUp(self):
        self.organization = factories.Organization(id=1)
        self.tola_user = factories.TolaUser(organization=self.organization)
        factories.Dashboard(user=self.tola_user)
        self.factory = APIRequestFactory()

    def test_list_dashboard_normal_user(self):
        request = self.factory.get('')
        request.user = self.tola_user.user
        view = DashboardViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], u'My crazy Dashboard')


class DashboardCreateViewTest(TestCase):
    def setUp(self):
        self.organization = factories.Organization(id=1)
        self.tola_user = factories.TolaUser(organization=self.organization)
        self.factory = APIRequestFactory()

    def test_create_dashboard(self):
        request = self.factory.post('/api/dashboard/')
        user_url = reverse('user-detail', kwargs={'pk': self.tola_user.user.id},
                           request=request)

        data = {'name': 'YoDash', 'user': user_url}
        request = self.factory.post('/api/dashboard/', data)
        request.user = self.tola_user.user
        view = DashboardViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 400)

    def test_create_dashboard_json(self):
        request = self.factory.post('/api/dashboard/')
        user_url = reverse('user-detail', kwargs={'pk': self.tola_user.user.pk},
                           request=request)

        data = {'name': 'YoDash', 'user': user_url}
        request = self.factory.post(
            '/api/dashboard/', json.dumps(data), content_type='application/json')
        request.user = self.tola_user.user
        view = DashboardViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 400)
