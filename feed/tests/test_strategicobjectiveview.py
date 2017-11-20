from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import StrategicObjectiveViewSet


class StrategicObjectiveListViewTest(TestCase):
    def setUp(self):
        factories.StrategicObjective.create_batch(2)
        self.tola_user = factories.TolaUser()
        self.factory = APIRequestFactory()

    def test_list_strategicobjective_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.get('/api/strategicobjective/')
        request.user = self.tola_user.user
        view = StrategicObjectiveViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_strategicobjective_normaluser(self):
        request = self.factory.get('/api/strategicobjective/')
        request.user = self.tola_user.user
        view = StrategicObjectiveViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_strategicobjective_normaluser_one_result(self):

        factories.StrategicObjective(
            name='StrategicObjective0',
            organization=self.tola_user.organization)
        request = self.factory.get('/api/strategicobjective/')
        request.user = self.tola_user.user
        view = StrategicObjectiveViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class StrategicObjectiveCreateViewTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()
        self.factory = APIRequestFactory()
            
    def test_create_strategicobjective_normaluser_one_result(self):
        request = self.factory.post('/api/strategicobjective/')
        request.user = self.tola_user.user
        view = StrategicObjectiveViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)

        # check if the obj created has the user organization
        request = self.factory.get('/api/strategicobjective/')
        request.user = self.tola_user.user
        view = StrategicObjectiveViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class StrategicObjectiveFilterViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_filter_strategicobjective_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        another_org = factories.Organization(name='Another Org')
        s_obj1 = factories.StrategicObjective(
            name='StrategicObjective1',
            organization=self.tola_user.organization)
        factories.StrategicObjective(name='StrategicObjective2',
                                     organization=another_org)

        request = self.factory.get(
            '/api/strategicobjective/?organization__id=%s' %
            self.tola_user.organization.pk)
        request.user = self.tola_user.user
        view = StrategicObjectiveViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], s_obj1.name)

    def test_filter_strategicobjective_normaluser(self):
        country1 = factories.Country(country='Brazil', code='BR')
        country2 = factories.Country()
        s_obj1 = factories.StrategicObjective(
            name='StrategicObjective1',
            country=country1,
            organization=self.tola_user.organization
        )
        factories.StrategicObjective(
            name='StrategicObjective2',
            country=country2,
            organization=self.tola_user.organization
        )

        request = self.factory.get(
            '/api/strategicobjective/?country__country=%s' %
            country1.country)
        request.user = self.tola_user.user
        view = StrategicObjectiveViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], s_obj1.name)
