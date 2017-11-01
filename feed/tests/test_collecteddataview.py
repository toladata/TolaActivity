from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import factories
from feed.views import CollectedDataViewSet


class CollectedDataViewTest(TestCase):
    def setUp(self):
        self.user = factories.User(is_superuser=True, is_staff=True)
        tola_user = factories.TolaUser(user=self.user)
        self.organization = tola_user.organization
        factory = APIRequestFactory()
        self.request = factory.post('/api/collecteddata/')

    def test_create_collecteddata(self):
        wflvl1 = factories.WorkflowLevel1()
        indicator = factories.Indicator.create(workflowlevel1=(wflvl1,))
        indicator_url = reverse('indicator-detail', kwargs={'pk': indicator.id},
                                request=self.request)
        user_url = reverse('user-detail', kwargs={'pk': self.user.id},
                           request=self.request)

        data = {'indicator': indicator_url}
        self.request = APIRequestFactory().post('/api/collecteddata/', data)
        self.request.user = self.user
        view = CollectedDataViewSet.as_view({'post': 'create'})
        response = view(self.request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['owner'], user_url)
