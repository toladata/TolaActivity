from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import TolaUserViewSet


class TolaUserListViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

        self.tola_user_ringo = factories.TolaUser(
            user=factories.User(first_name='Ringo', last_name='Starr'),
            organization=self.tola_user.organization)
        self.tola_user_george = factories.TolaUser(
            user=factories.User(first_name='George', last_name='Harrison'),
            organization=factories.Organization(name='Other Org'))

    def test_list_tolauser_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.get('')
        request.user = self.tola_user.user
        view = TolaUserViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

        for i, name in enumerate((u'George Harrison', u'Ringo Starr',
                                  u'Thom Yorke')):
            self.assertEqual(response.data[i]['name'], name)

    def test_list_tolauser_other_user(self):
        request = self.factory.get('')
        request.user = self.tola_user.user
        view = TolaUserViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        for i, name in enumerate((u'Ringo Starr', u'Thom Yorke')):
            self.assertEqual(response.data[i]['name'], name)
