from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from feed.views import ContactViewSet
from workflow.models import Contact, Country, Organization, TolaUser, \
    WorkflowLevel1, WorkflowTeam


class ContactViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com',
                                             'johnpassword')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.country = Country.objects.create(country='Afghanistan', code='AF')

        Contact.objects.bulk_create([
            Contact(name='Contact_0', country=self.country),
            Contact(name='Contact_1', country=self.country),
        ])

        factory = APIRequestFactory()
        self.request = factory.get('/api/contact/')

    def test_list_contact_superuser(self):
        self.request.user = self.user
        view = ContactViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_contact_normaluser(self):
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save()
        organization = Organization.objects.create(name="TestOrg")
        TolaUser.objects.create(user=self.user, organization=organization)

        self.request.user = self.user
        view = ContactViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_contact_normaluser_one_result(self):
        self.user.is_superuser = False
        self.user.is_staff = False
        self.user.save()
        organization = Organization.objects.create(name="TestOrg")
        tola_user = TolaUser.objects.create(user=self.user,
                                            organization=organization)

        wflvl1 = WorkflowLevel1.objects.create(name='WorkflowLevel1',
                                               organization=organization)
        WorkflowTeam.objects.create(workflow_user=tola_user,
                                    workflowlevel1=wflvl1)
        Contact.objects.create(name='Contact_0', country=self.country,
                               organization=organization,
                               workflowlevel1=wflvl1)

        self.request.user = self.user
        view = ContactViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
