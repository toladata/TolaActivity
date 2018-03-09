import json

from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import DashboardViewSet
from workflow.models import Dashboard


class DashboardListViewTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()
        self.factory = APIRequestFactory()
        factories.Dashboard.create_batch(2)

    def test_list_dashboard_super_user(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.get('')
        request.user = self.tola_user.user
        view = DashboardViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_dashboard_created_by(self):
        user = factories.User(first_name='John', last_name='Lennon')
        tola_user = factories.TolaUser(user=user)
        factories.Dashboard(name='My New Dashboard', user=tola_user)

        request = self.factory.get('')
        request.user = tola_user.user
        view = DashboardViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], u'My New Dashboard')

    def test_list_dashboard_shared_with(self):
        user = factories.User(first_name='John', last_name='Lennon')
        tola_user = factories.TolaUser(user=user)
        factories.Dashboard(name='My New Dashboard', user=self.tola_user,
                            share=[tola_user])

        request = self.factory.get('')
        request.user = tola_user.user
        view = DashboardViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], u'My New Dashboard')

    def test_list_dashboard_public_org(self):
        user = factories.User(first_name='John', last_name='Lennon')
        tola_user = factories.TolaUser(
            user=user, organization=self.tola_user.organization)
        factories.Dashboard(name='My Org Dashboard', user=self.tola_user,
                            public=Dashboard.PUBLIC_ORG)

        request = self.factory.get('')
        request.user = tola_user.user
        view = DashboardViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], u'My Org Dashboard')

    def test_list_dashboard_public_all(self):
        another_org = factories.Organization()
        org = self.tola_user.organization
        self.tola_user.organization = another_org
        self.tola_user.save()

        user = factories.User(first_name='John', last_name='Lennon')
        tola_user = factories.TolaUser(user=user, organization=org)
        factories.Dashboard(name='Another Org Dashboard', user=self.tola_user,
                            public=Dashboard.PUBLIC_ALL)

        request = self.factory.get('')
        request.user = tola_user.user
        view = DashboardViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], u'Another Org Dashboard')


class DashboardCreateViewTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()
        self.factory = APIRequestFactory()

    def test_create_dashboard_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        data = {'name': 'YoDash'}
        request = self.factory.post('/api/dashboard/', data)
        request.user = self.tola_user.user
        view = DashboardViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'YoDash')
        self.assertEqual(response.data['user'].name, self.tola_user.name)

    def test_create_dashboard_json(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        data = {'name': 'YoDash'}
        request = self.factory.post('/api/dashboard/', json.dumps(data),
                                    content_type='application/json')
        request.user = self.tola_user.user
        view = DashboardViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'YoDash')
        self.assertEqual(response.data['user'].name, self.tola_user.name)


class DashboardFilterViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        factories.Dashboard.create_batch(2)

    def test_filter_dashboard_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.get('?public={}'.format(Dashboard.PUBLIC_ORG))
        request.user = self.tola_user.user
        view = DashboardViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_filter_dashboard_public_all(self):
        another_org = factories.Organization()
        org = self.tola_user.organization
        self.tola_user.organization = another_org
        self.tola_user.save()
        user_1 = factories.User(first_name='John', last_name='Lennon')
        user_2 = factories.User(first_name='Paul', last_name='McCartney')
        tolauser_1 = factories.TolaUser(user=user_1, organization=org)
        tolauser_2 = factories.TolaUser(user=user_2, organization=org)

        factories.Dashboard(name='My Org Dashboard', user=tolauser_1,
                            public=Dashboard.PUBLIC_ORG)
        factories.Dashboard(name='Another Org Dashboard', user=self.tola_user,
                            public=Dashboard.PUBLIC_ALL)

        request = self.factory.get('?public={}'.format(Dashboard.PUBLIC_ALL))
        request.user = tolauser_2.user
        view = DashboardViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], u'Another Org Dashboard')
        self.assertNotEqual(response.data[0]['name'], u'My Org Dashboard')

    def test_filter_dashboard_public_org(self):
        another_org = factories.Organization()
        org = self.tola_user.organization
        self.tola_user.organization = another_org
        self.tola_user.save()
        user_1 = factories.User(first_name='John', last_name='Lennon')
        user_2 = factories.User(first_name='Paul', last_name='McCartney')
        tolauser_1 = factories.TolaUser(user=user_1, organization=org)
        tolauser_2 = factories.TolaUser(user=user_2, organization=org)

        factories.Dashboard(name='My Org Dashboard', user=tolauser_1,
                            public=Dashboard.PUBLIC_ORG)
        factories.Dashboard(name='Another Org Dashboard', user=self.tola_user,
                            public=Dashboard.PUBLIC_ALL)

        request = self.factory.get('?public={}'.format(Dashboard.PUBLIC_ORG))
        request.user = tolauser_2.user
        view = DashboardViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], u'My Org Dashboard')
        self.assertNotEqual(response.data[0]['name'], u'Another Org Dashboard')

    def test_filter_dashboard_share_with(self):
        user = factories.User(first_name='John', last_name='Lennon')
        tolauser = factories.TolaUser(
            user=user, organization=self.tola_user.organization)

        factories.Dashboard(name='My Dashboard', user=tolauser)
        factories.Dashboard(name='Not shared Dashboard', user=self.tola_user)
        factories.Dashboard(name='Shared Dashboard', user=self.tola_user,
                            share=[tolauser])

        request = self.factory.get('?share={}'.format(tolauser.id))
        request.user = tolauser.user
        view = DashboardViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], u'Shared Dashboard')
        self.assertNotEqual(response.data[0]['name'], u'Not shared Dashboard')
        self.assertNotEqual(response.data[0]['name'], u'My Dashboard')

    def test_filter_dashboard_created_by(self):
        user = factories.User(first_name='John', last_name='Lennon')
        tolauser = factories.TolaUser(
            user=user, organization=self.tola_user.organization)

        factories.Dashboard(name='My Dashboard', user=tolauser)
        factories.Dashboard(name='Shared Dashboard', user=self.tola_user,
                            share=[tolauser])

        request = self.factory.get('?user={}'.format(tolauser.id))
        request.user = tolauser.user
        view = DashboardViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], u'My Dashboard')
        self.assertNotEqual(response.data[0]['name'], u'Shared Dashboard')
