from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import factories
from feed.views import SiteProfileViewSet
from workflow.models import SiteProfile


class SiteProfileViewsTest(TestCase):
    def setUp(self):
        self.country = factories.Country()
        SiteProfile.objects.bulk_create([
            SiteProfile(name='SiteProfile1', country=self.country),
            SiteProfile(name='SiteProfile2', country=self.country),
        ])

        factory = APIRequestFactory()
        self.request_get = factory.get('/api/siteprofile/')
        self.request_post = factory.post('/api/siteprofile/')

    def test_list_siteprofile_superuser(self):
        self.request_get.user = factories.User.build(is_superuser=True,
                                                     is_staff=True)
        view = SiteProfileViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_siteprofile_normaluser(self):
        tola_user = factories.TolaUser()

        self.request_get.user = tola_user.user
        view = SiteProfileViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_siteprofile_normaluser_one_result(self):
        tola_user = factories.TolaUser()

        SiteProfile.objects.create(name='SiteProfile0',
                                   organization=tola_user.organization,
                                   country=self.country)

        self.request_get.user = tola_user.user
        view = SiteProfileViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
    
    def test_create_siteprofile_normaluser_one_result(self):
        tola_user = factories.TolaUser()
        user_url = reverse('user-detail', kwargs={'pk': tola_user.user.id},
                           request=self.request_post)

        data = {
            'name': 'Site Profile 1',
            'country': 'http://testserver/api/country/%s/' % self.country.id
        }
        self.request_post = APIRequestFactory().post('/api/siteprofile/', data)
        self.request_post.user = tola_user.user
        view = SiteProfileViewSet.as_view({'post': 'create'})
        response = view(self.request_post)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['owner'], user_url)

        # check if the obj created has the user organization
        self.request_get.user = tola_user.user
        view = SiteProfileViewSet.as_view({'get': 'list'})
        response = view(self.request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_filter_siteprofile_normaluser_one_result(self):
        tola_user = factories.TolaUser()

        site = SiteProfile.objects.create(name='SiteProfile0',
                                          organization=tola_user.organization,
                                          country=self.country)
        wkf1 = factories.WorkflowLevel1()
        wkf2 = factories.WorkflowLevel2.create(workflowlevel1=wkf1)
        wkf2.site.add(site)

        path = \
            '/api/siteprofile/?workflowlevel2__workflowlevel1=%s' % wkf1.id
        request_get = APIRequestFactory().get(path)
        request_get.user = tola_user.user
        view = SiteProfileViewSet.as_view({'get': 'list'})
        response = view(request_get)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
