from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from feed.views import StrategicObjectiveViewSet
from indicators.models import StrategicObjective
from workflow.models import Organization, TolaUser


class StrategicObjectiveViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

        StrategicObjective.objects.bulk_create([
            StrategicObjective(name='StrategicObjective1'),
            StrategicObjective(name='StrategicObjective2'),
        ])

        factory = APIRequestFactory()
        self.request_get = factory.get('/api/strategicobjective/')
        self.request_post = factory.post('/api/strategicobjective/')

    def test_list_strategicobjective_superuser(self):
        self.request_get.user = self.user
        view = StrategicObjectiveViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_strategicobjective_normaluser(self):
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save()
        organization = Organization.objects.create(name="TestOrg")
        TolaUser.objects.create(user=self.user, organization=organization)

        self.request_get.user = self.user
        view = StrategicObjectiveViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_strategicobjective_normaluser_one_result(self):
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save()
        organization = Organization.objects.create(name="TestOrg")
        TolaUser.objects.create(user=self.user, organization=organization)

        StrategicObjective.objects.create(name='StrategicObjective0', organization=organization)

        self.request_get.user = self.user
        view = StrategicObjectiveViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
    
    def test_create_strategicobjective_normaluser_one_result(self):
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save()
        organization = Organization.objects.create(name="TestOrg")
        TolaUser.objects.create(user=self.user, organization=organization)

        self.request_post.user = self.user
        view = StrategicObjectiveViewSet.as_view({'post': 'create'})
        response = view(self.request_post)
        self.assertEqual(response.status_code, 201)

        # check if the obj created has the user organization
        self.request_get.user = self.user
        view = StrategicObjectiveViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
