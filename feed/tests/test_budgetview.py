from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import factories
from feed.views import BudgetViewSet


class BudgetViewTest(TestCase):
    def setUp(self):
        self.user = factories.User(is_superuser=True, is_staff=True)
        factory = APIRequestFactory()
        self.request = factory.post('/api/budget/')

    def test_create_budget(self):
        user_url = reverse('user-detail', kwargs={'pk': self.user.id},
                           request=self.request)

        self.request.user = self.user
        view = BudgetViewSet.as_view({'post': 'create'})
        response = view(self.request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['owner'], user_url)
