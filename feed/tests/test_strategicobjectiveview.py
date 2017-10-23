from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import StrategicObjectiveViewSet
from indicators.models import StrategicObjective


class StrategicObjectiveViewsTest(TestCase):
    def setUp(self):
        StrategicObjective.objects.bulk_create([
            StrategicObjective(name='StrategicObjective1'),
            StrategicObjective(name='StrategicObjective2'),
        ])

        factory = APIRequestFactory()
        self.request_get = factory.get('/api/strategicobjective/')
        self.request_post = factory.post('/api/strategicobjective/')

    def test_list_strategicobjective_superuser(self):
        self.request_get.user = factories.User.build(is_superuser=True, is_staff=True)
        view = StrategicObjectiveViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_strategicobjective_normaluser(self):
        tola_user = factories.TolaUser()

        self.request_get.user = tola_user.user
        view = StrategicObjectiveViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_strategicobjective_normaluser_one_result(self):
        tola_user = factories.TolaUser()

        StrategicObjective.objects.create(name='StrategicObjective0', organization=tola_user.organization)

        self.request_get.user = tola_user.user
        view = StrategicObjectiveViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
    
    def test_create_strategicobjective_normaluser_one_result(self):
        tola_user = factories.TolaUser()

        self.request_post.user = tola_user.user
        view = StrategicObjectiveViewSet.as_view({'post': 'create'})
        response = view(self.request_post)
        self.assertEqual(response.status_code, 201)

        # check if the obj created has the user organization
        self.request_get.user = tola_user.user
        view = StrategicObjectiveViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
