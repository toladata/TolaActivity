from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import factories
from feed.views import IndicatorViewSet


class IndicatorViewTest(TestCase):
    def setUp(self):
        self.user = factories.User(is_superuser=True, is_staff=True)
        tola_user = factories.TolaUser(user=self.user)
        self.organization = tola_user.organization
        factory = APIRequestFactory()
        self.request = factory.post('/api/indicator/')

    def test_create_indicator(self):
        wflvl1 = factories.WorkflowLevel1()
        wflvl1_url = reverse('workflowlevel1-detail', kwargs={'pk': wflvl1.id},
                             request=self.request)
        user_url = reverse('user-detail', kwargs={'pk': self.user.id},
                           request=self.request)

        data = {'name': 'Building resilience in Mali',
                'workflowlevel1': wflvl1_url}
        self.request = APIRequestFactory().post('/api/indicator/', data)
        self.request.user = self.user
        view = IndicatorViewSet.as_view({'post': 'create'})
        response = view(self.request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Building resilience in Mali')
        self.assertEqual(response.data['created_by'], user_url)
