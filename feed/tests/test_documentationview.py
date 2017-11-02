from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import factories
from feed.views import DocumentationViewSet


class DocumentationViewTest(TestCase):
    def setUp(self):
        self.user = factories.User(is_superuser=True, is_staff=True)
        factories.TolaUser(user=self.user)
        factory = APIRequestFactory()
        self.request = factory.post('/api/documentation/')

    def test_create_documentation(self):
        wflvl1 = factories.WorkflowLevel1()
        wflvl1_url = reverse('workflowlevel1-detail', kwargs={'pk': wflvl1.id},
                             request=self.request)
        user_url = reverse('user-detail', kwargs={'pk': self.user.id},
                           request=self.request)

        data = {'name': 'Needs Assessment report',
                'workflowlevel1': wflvl1_url}
        self.request = APIRequestFactory().post('/api/documentation/', data)
        self.request.user = self.user
        view = DocumentationViewSet.as_view({'post': 'create'})
        response = view(self.request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Needs Assessment report')
        self.assertEqual(response.data['owner'], user_url)
