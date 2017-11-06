from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import IssueRegisterViewSet
from workflow.models import IssueRegister


class IssueRegisterViewsTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()
        IssueRegister.objects.bulk_create([
            IssueRegister(name='IssueRegister1'),
            IssueRegister(name='IssueRegister2'),
        ])

        factory = APIRequestFactory()
        self.request_get = factory.get('/api/issueregister/')
        self.request_get.user = self.tola_user.user
        self.request_post = factory.post('/api/issueregister/')
        self.request_post.user = self.tola_user.user

    def test_list_issueregister_superuser(self):
        self.request_get.user = factories.User.build(is_superuser=True, is_staff=True)
        view = IssueRegisterViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_issueregister_normaluser(self):
        view = IssueRegisterViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_issueregister_normaluser_one_result(self):
        IssueRegister.objects.create(name='IssueRegister0', organization=self.tola_user.organization)
        view = IssueRegisterViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
    
    def test_create_issueregister_normaluser_one_result(self):
        view = IssueRegisterViewSet.as_view({'post': 'create'})
        response = view(self.request_post)
        self.assertEqual(response.status_code, 201)

        # check if the obj created has the user organization
        view = IssueRegisterViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
