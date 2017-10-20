from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import IssueRegisterViewSet
from workflow.models import IssueRegister, TolaUser


class IssueRegisterViewsTest(TestCase):
    def setUp(self):
        IssueRegister.objects.bulk_create([
            IssueRegister(name='IssueRegister1'),
            IssueRegister(name='IssueRegister2'),
        ])

        factory = APIRequestFactory()
        self.request_get = factory.get('/api/issueregister/')
        self.request_post = factory.post('/api/issueregister/')

    def test_list_issueregister_superuser(self):
        self.request_get.user = factories.User.build(is_superuser=True, is_staff=True)
        view = IssueRegisterViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_issueregister_normaluser(self):
        user = factories.User()
        organization = factories.Organization()
        TolaUser.objects.create(user=user, organization=organization)

        self.request_get.user = user
        view = IssueRegisterViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_issueregister_normaluser_one_result(self):
        user = factories.User()
        organization = factories.Organization()
        TolaUser.objects.create(user=user, organization=organization)

        IssueRegister.objects.create(name='IssueRegister0', organization=organization)

        self.request_get.user = user
        view = IssueRegisterViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
    
    def test_create_issueregister_normaluser_one_result(self):
        user = factories.User()
        organization = factories.Organization()
        TolaUser.objects.create(user=user, organization=organization)

        self.request_post.user = user
        view = IssueRegisterViewSet.as_view({'post': 'create'})
        response = view(self.request_post)
        self.assertEqual(response.status_code, 201)

        # check if the obj created has the user organization
        self.request_get.user = user
        view = IssueRegisterViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
