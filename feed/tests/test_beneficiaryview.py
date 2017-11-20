from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import BeneficiaryViewSet
from workflow.models import WorkflowTeam, ROLE_ORGANIZATION_ADMIN, \
    ROLE_PROGRAM_TEAM, ROLE_PROGRAM_ADMIN, ROLE_VIEW_ONLY


class BeneficiaryListViewsTest(TestCase):
    def setUp(self):
        factories.Beneficiary.create_batch(2)
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_list_beneficiary_superuser(self):
        request = self.factory.get('/api/beneficiary/')
        request.user = factories.User.build(is_superuser=True,
                                            is_staff=True)
        view = BeneficiaryViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_beneficiary_org_admin(self):
        request = self.factory.get('/api/beneficiary/')
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request.user = self.tola_user.user
        view = BeneficiaryViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        wkflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        factories.Beneficiary(workflowlevel1=[wkflvl1])
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_beneficiary_program_admin(self):
        request = self.factory.get('/api/beneficiary/')
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))
        request.user = self.tola_user.user
        view = BeneficiaryViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        wkflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        factories.Beneficiary(workflowlevel1=[wkflvl1])
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_beneficiary_program_team(self):
        request = self.factory.get('/api/beneficiary/')
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            role=factories.Group(name=ROLE_PROGRAM_TEAM))
        request.user = self.tola_user.user
        view = BeneficiaryViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        wkflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        factories.Beneficiary(workflowlevel1=[wkflvl1])
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_beneficiary_view_only(self):
        request = self.factory.get('/api/beneficiary/')
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            role=factories.Group(name=ROLE_VIEW_ONLY))
        request.user = self.tola_user.user
        view = BeneficiaryViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

        wkflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        factories.Beneficiary(workflowlevel1=[wkflvl1])
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class BeneficiaryFilterViewTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()
        self.factory = APIRequestFactory()

    def test_filter_beneficiary_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        another_org = factories.Organization(name='Another Org')
        wkflvl1_1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wkflvl1_2 = factories.WorkflowLevel1(
            organization=another_org)
        beneficiary1 = factories.Beneficiary(workflowlevel1=[wkflvl1_1])
        factories.Beneficiary(
            beneficiary_name='James McCartney', father_name='Paul McCartney',
            workflowlevel1=[wkflvl1_2])

        request = self.factory.get(
            '/api/beneficiary/?workflowlevel1__organization__id=%s' %
            self.tola_user.organization.pk)
        request.user = self.tola_user.user
        view = BeneficiaryViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['beneficiary_name'],
                         beneficiary1.beneficiary_name)
