from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import json
from feed.views import ContactViewSet
import factories
from workflow.models import Contact, WorkflowLevel1, WorkflowTeam, \
    ROLE_ORGANIZATION_ADMIN, ROLE_PROGRAM_TEAM, ROLE_PROGRAM_ADMIN, \
    ROLE_VIEW_ONLY


class ContactListViewTest(TestCase):
    def setUp(self):
        factories.Contact.create_batch(2)
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_list_contact_superuser(self):
        request = self.factory.get('/api/contact/')
        request.user = factories.User.build(is_superuser=True,
                                            is_staff=True)
        view = ContactViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_contact_normaluser(self):
        request = self.factory.get('/api/contact/')
        request.user = self.tola_user.user
        view = ContactViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_contact_normaluser_one_result(self):
        request = self.factory.get('/api/contact/')
        wflvl1 = WorkflowLevel1.objects.create(
            name='WorkflowLevel1', organization=self.tola_user.organization)
        WorkflowTeam.objects.create(workflow_user=self.tola_user,
                                    workflowlevel1=wflvl1)
        factories.Contact(organization=self.tola_user.organization,
                          workflowlevel1=wflvl1)

        request.user = self.tola_user.user
        view = ContactViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class ContactCreateViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_create_contact_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.post('/api/contact/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail', kwargs={'pk': wflvl1.id},
                             request=request)
        organization_url = reverse('organization-detail',
                                   kwargs={'pk': self.tola_user.organization.id}
                                   , request=request)
        country_url = reverse('country-detail',
                              kwargs={'pk': self.tola_user.country.id},
                              request=request)

        data = {'name': 'John Lennon',
                'city': 'Liverpool',
                'country': country_url,
                'workflowlevel1': wflvl1_url,
                'organization': organization_url}

        request = self.factory.post('/api/contact/', data)
        request.user = self.tola_user.user
        view = ContactViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'John Lennon')

    def test_create_contact_program_admin(self):
        request = self.factory.post('/api/contact/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail', kwargs={'pk': wflvl1.id},
                             request=request)
        organization_url = reverse('organization-detail',
                                   kwargs={'pk': self.tola_user.organization.id}
                                   , request=request)
        country_url = reverse('country-detail',
                              kwargs={'pk': self.tola_user.country.id},
                              request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        data = {'name': 'John Lennon',
                'city': 'Liverpool',
                'country': country_url,
                'workflowlevel1': wflvl1_url,
                'organization': organization_url}

        request = self.factory.post('/api/contact/', data)
        request.user = self.tola_user.user
        view = ContactViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'John Lennon')

    def test_create_contact_program_admin_json(self):
        request = self.factory.post('/api/contact/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail', kwargs={'pk': wflvl1.id},
                             request=request)
        organization_url = reverse('organization-detail',
                                   kwargs={'pk': self.tola_user.organization.id}
                                   , request=request)
        country_url = reverse('country-detail',
                              kwargs={'pk': self.tola_user.country.id},
                              request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        data = {'name': 'John Lennon',
                'city': 'Liverpool',
                'country': country_url,
                'workflowlevel1': wflvl1_url,
                'organization': organization_url}

        request = self.factory.post('/api/contact/', json.dumps(data),
                                    content_type='application/json')
        request.user = self.tola_user.user
        view = ContactViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'John Lennon')


class ContactDeleteViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_delete_contact_non_existing(self):
        request = self.factory.delete('/api/contact/')
        request.user = self.tola_user.user
        view = ContactViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=288)
        self.assertEquals(response.status_code, 404)

    def test_delete_contact_superuser(self):
        self.tola_user.user.is_superuser = True
        self.tola_user.user.is_staff = True
        self.tola_user.user.save()

        contact = factories.Contact()
        request = self.factory.delete('/api/contact/')
        request.user = self.tola_user.user
        view = ContactViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=contact.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Contact.DoesNotExist,
            Contact.objects.get, pk=contact.pk)

    def test_delete_contact_org_admin(self):
        contact = factories.Contact(organization=self.tola_user.organization)
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.delete('/api/contact/')
        request.user = self.tola_user.user
        view = ContactViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=contact.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Contact.DoesNotExist,
            Contact.objects.get, pk=contact.pk)

    def test_delete_contact_diff_org_org_admin(self):
        another_org = factories.Organization(name='Another Org')
        contact = factories.Contact(organization=another_org)
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.delete('/api/contact/')
        request.user = self.tola_user.user
        view = ContactViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=contact.pk)
        self.assertEquals(response.status_code, 403)
        Contact.objects.get(pk=contact.pk)

    def test_delete_contact_program_admin(self):
        contact = factories.Contact(organization=self.tola_user.organization)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=factories.WorkflowLevel1(
                organization=self.tola_user.organization),
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        request = self.factory.delete('/api/contact/')
        request.user = self.tola_user.user
        view = ContactViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=contact.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Contact.DoesNotExist,
            Contact.objects.get, pk=contact.pk)

    def test_delete_contact_diff_org_program_admin(self):
        another_org = factories.Organization(name='Another Org')
        contact = factories.Contact(organization=another_org)
        group_org_admin = factories.Group(name=ROLE_PROGRAM_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.delete('/api/contact/')
        request.user = self.tola_user.user
        view = ContactViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=contact.pk)
        self.assertEquals(response.status_code, 403)
        Contact.objects.get(pk=contact.pk)

    def test_delete_contact_normal_user(self):
        contact = factories.Contact()

        request = self.factory.delete('/api/contact/')
        request.user = self.tola_user.user
        view = ContactViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=contact.pk)
        self.assertEquals(response.status_code, 403)
        Contact.objects.get(pk=contact.pk)


class ContactFilterViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_filter_contact_stakeholder_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        wkflvl1 = factories.WorkflowLevel1()
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wkflvl1)
        contact1 = factories.Contact(name='John',
                                     organization=self.tola_user.organization,
                                     workflowlevel1=wkflvl1)
        factories.Contact(name='Paul',
                          organization=self.tola_user.organization,
                          workflowlevel1=wkflvl1)
        request = self.factory.get('/api/contact/?name=%s' % contact1.name)
        request.user = self.tola_user.user
        view = ContactViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], contact1.name)
