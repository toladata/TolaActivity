from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import json
import factories
from feed.views import SiteProfileViewSet
from workflow.models import SiteProfile


class SiteProfileListViewTest(TestCase):
    def setUp(self):
        self.country = factories.Country()
        SiteProfile.objects.bulk_create([
            SiteProfile(name='SiteProfile1', country=self.country),
            SiteProfile(name='SiteProfile2', country=self.country),
        ])
        factories.Indicator.create_batch(2)

        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_list_siteprofile_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()
        
        request = self.factory.get('/api/siteprofile/')
        request.user = self.tola_user.user
        view = SiteProfileViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_siteprofile_normaluser(self):
        request = self.factory.get('/api/siteprofile/')
        request.user = self.tola_user.user
        view = SiteProfileViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_siteprofile_normaluser_one_result(self):
        SiteProfile.objects.create(name='SiteProfile0',
                                   organization=self.tola_user.organization,
                                   country=self.country)

        request = self.factory.get('/api/siteprofile/')
        request.user = self.tola_user.user
        view = SiteProfileViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class SiteProfileCreateViewTest(TestCase):
    def setUp(self):
        self.country = factories.Country()
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
            
    def test_create_siteprofile_normaluser_one_result(self):
        request = self.factory.post('/api/siteprofile/')
        user_url = reverse('user-detail', kwargs={'pk': self.tola_user.user.id},
                           request=request)
        wflvl1_1 = factories.WorkflowLevel1()
        wflvl1_2 = factories.WorkflowLevel1()
        wflvl1_1_url = reverse('workflowlevel1-detail',
                               kwargs={'pk': wflvl1_1.id},
                               request=request)
        wflvl1_2_url = reverse('workflowlevel1-detail',
                               kwargs={'pk': wflvl1_2.id},
                               request=request)
        country_url = reverse('country-detail',
                              kwargs={'pk': self.country.id},
                              request=request)

        data = {
            'name': 'Site Profile 1',
            'country': country_url,
            'workflowlevel1': [wflvl1_1_url, wflvl1_2_url]
        }
        request = self.factory.post('/api/siteprofile/', data)
        request.user = self.tola_user.user
        view = SiteProfileViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['created_by'], user_url)

        # check if the obj created has the user organization
        request = self.factory.get('/api/siteprofile/')
        request.user = self.tola_user.user
        view = SiteProfileViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_siteprofile_normaluser_one_result_json(self):
        request = self.factory.post('/api/siteprofile/')
        user_url = reverse('user-detail', kwargs={'pk': self.tola_user.user.id},
                           request=request)
        wflvl1_1 = factories.WorkflowLevel1()
        wflvl1_2 = factories.WorkflowLevel1()
        wflvl1_1_url = reverse('workflowlevel1-detail',
                               kwargs={'pk': wflvl1_1.id},
                               request=request)
        wflvl1_2_url = reverse('workflowlevel1-detail',
                               kwargs={'pk': wflvl1_2.id},
                               request=request)
        country_url = reverse('country-detail',
                              kwargs={'pk': self.country.id},
                              request=request)

        data = {
            'name': 'Site Profile 1',
            'country': country_url,
            'workflowlevel1': [wflvl1_1_url, wflvl1_2_url]
        }
        request = self.factory.post('/api/siteprofile/', json.dumps(data),
                                    content_type='application/json')
        request.user = self.tola_user.user
        view = SiteProfileViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['created_by'], user_url)

        # check if the obj created has the user organization
        request = self.factory.get('/api/siteprofile/')
        request.user = self.tola_user.user
        view = SiteProfileViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class SiteProfileFilterViewTest(TestCase):
    def setUp(self):
        self.country = factories.Country(country='Brazil', code='BR')
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_filter_siteprofile_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        site1 = factories.SiteProfile(name='SiteProfile1',
                                        country=self.country)
        factories.SiteProfile(name='SiteProfile2', country=factories.Country())

        request = self.factory.get('/api/siteprofile/?country__country=%s' %
                                   self.country.country)
        request.user = self.tola_user.user
        view = SiteProfileViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], site1.name)

    def test_filter_siteprofile_normaluser(self):
        site1 = factories.SiteProfile(
            name='SiteProfile1', country=self.country,
            organization=self.tola_user.organization)
        factories.SiteProfile(name='SiteProfile2', country=factories.Country(),
                              organization=self.tola_user.organization)

        request = self.factory.get('/api/siteprofile/?country__country=%s' %
                                   self.country.country)
        request.user = self.tola_user.user
        view = SiteProfileViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], site1.name)
