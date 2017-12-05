from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import json
import factories
from feed.views import SectorViewSet


class SectorCreateViewTest(TestCase):
    def setUp(self):
        self.organization = factories.Organization(id=1)
        self.tola_user = factories.TolaUser(organization=self.organization)
        self.factory = APIRequestFactory()

    def test_create_sector(self):
        request = self.factory.post('/api/sector/')
        user_url = reverse('user-detail', kwargs={'pk': self.tola_user.user.id},
                           request=request)

        data = {'sector': 'Agriculture'}
        request = self.factory.post('/api/sector/', data)
        request.user = self.tola_user.user
        view = SectorViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['sector'], u'Agriculture')
        self.assertEqual(response.data['created_by'], user_url)

    def test_create_sector_json(self):
        request = self.factory.post('/api/sector/')
        user_url = reverse('user-detail', kwargs={'pk': self.tola_user.user.pk},
                           request=request)

        data = {'sector': 'Agriculture'}
        request = self.factory.post(
            '/api/sector/', json.dumps(data), content_type='application/json')
        request.user = self.tola_user.user
        view = SectorViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['sector'], u'Agriculture')
        self.assertEqual(response.data['created_by'], user_url)


class SectorFilterViewTest(TestCase):
    def setUp(self):
        self.organization = factories.Organization(id=1)
        self.tola_user = factories.TolaUser(organization=self.organization)
        self.factory = APIRequestFactory()

    def test_filter_sector_superuser(self):
        another_org = factories.Organization(name='Another Org')
        sector1 = factories.Sector(organization=self.tola_user.organization)
        factories.Sector(sector='Another Sector', organization=another_org)

        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.get('/api/sector/?organization__id=%s' %
                                   self.tola_user.organization.pk)
        request.user = self.tola_user.user
        view = SectorViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['sector'], sector1.sector)

    def test_filter_sector_normaluser(self):
        another_org = factories.Organization(name='Another Org')
        sector1 = factories.Sector(organization=self.tola_user.organization)
        factories.Sector(sector='Another Sector', organization=another_org)

        request = self.factory.get('/api/sector/?organization__id=%s' %
                                   self.tola_user.organization.pk)
        request.user = self.tola_user.user
        view = SectorViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['sector'], sector1.sector)
