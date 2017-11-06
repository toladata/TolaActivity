from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import factories
from feed.views import MilestoneViewSet


class MilestoneViewTest(TestCase):
    def setUp(self):
        self.user = factories.User(is_superuser=True, is_staff=True)
        factory = APIRequestFactory()
        self.request = factory.post('/api/milestone/')

    def test_create_milestone(self):
        user_url = reverse('user-detail', kwargs={'pk': self.user.id},
                           request=self.request)

        data = {'name': 'Project Implementation'}
        self.request = APIRequestFactory().post('/api/milestone/', data)
        self.request.user = self.user
        view = MilestoneViewSet.as_view({'post': 'create'})
        response = view(self.request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Project Implementation')
        self.assertEqual(response.data['created_by'], user_url)
