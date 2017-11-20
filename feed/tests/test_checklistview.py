from django.test import TestCase
from django.test.utils import override_settings
from rest_framework.test import APIRequestFactory

import factories
from feed.views import ChecklistViewSet
from workflow.models import Checklist, WorkflowLevel1, WorkflowLevel2, \
    WorkflowTeam, ROLE_ORGANIZATION_ADMIN


class ChecklistListViewTest(TestCase):
    def setUp(self):
        wflvl1 = WorkflowLevel1.objects.create(name='WorkflowLevel1')
        wflvl2 = WorkflowLevel2.objects.create(name='WorkflowLevel2',
                                               workflowlevel1=wflvl1)
        Checklist.objects.bulk_create([
            Checklist(name='CheckList_0', workflowlevel2=wflvl2),
            Checklist(name='CheckList_1', workflowlevel2=wflvl2),
        ])

        factory = APIRequestFactory()
        self.request = factory.get('/api/checklist/')

    def test_list_checklist_superuser(self):
        self.request.user = factories.User.build(is_superuser=True,
                                                 is_staff=True)
        view = ChecklistViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_checklist_normaluser(self):
        tola_user = factories.TolaUser()
        self.request.user = tola_user.user
        view = ChecklistViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_checklist_normaluser_one_result(self):
        tola_user = factories.TolaUser()
        wflvl1 = WorkflowLevel1.objects.create(
            name='WorkflowLevel1', organization=tola_user.organization)
        wflvl2 = WorkflowLevel2.objects.create(name='WorkflowLevel2',
                                               workflowlevel1=wflvl1)
        Checklist.objects.create(name='CheckList_0', workflowlevel2=wflvl2)

        self.request.user = tola_user.user
        view = ChecklistViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class ChecklistFilterViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_filter_checklist_org_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        another_org = factories.Organization(name='Another Org')
        wkflvl1_1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wkflvl1_2 = factories.WorkflowLevel1(organization=another_org)
        wkflvl2_1 = factories.WorkflowLevel2(workflowlevel1=wkflvl1_1)
        wkflvl2_2 = factories.WorkflowLevel2(workflowlevel1=wkflvl1_2)
        checklist1 = factories.Checklist(name='Checklist A',
                                         workflowlevel2=wkflvl2_1)
        factories.Checklist(name='Checklist B',
                                         workflowlevel2=wkflvl2_2)

        request = self.factory.get(
            '/api/checklist/?workflowlevel2__workflowlevel1__organization__id'
            '=%s' % self.tola_user.organization.pk)
        request.user = self.tola_user.user
        view = ChecklistViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], checklist1.name)

    def test_filter_checklist_country_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        country1 = factories.Country(country='Brazil', code='BR')
        country2 = factories.Country(country='Germany', code='DE')
        wkflvl1_1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization, country=[country1])
        wkflvl1_2 = factories.WorkflowLevel1(
            organization=self.tola_user.organization, country=[country2])
        wkflvl2_1 = factories.WorkflowLevel2(workflowlevel1=wkflvl1_1)
        wkflvl2_2 = factories.WorkflowLevel2(workflowlevel1=wkflvl1_2)
        checklist1 = factories.Checklist(name='Checklist A',
                                         workflowlevel2=wkflvl2_1)
        factories.Checklist(name='Checklist B',
                                         workflowlevel2=wkflvl2_2)

        request = self.factory.get(
            '/api/checklist'
            '/?workflowlevel2__workflowlevel1__country__country=%s'
            % country1.country)
        request.user = self.tola_user.user
        view = ChecklistViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], checklist1.name)

    def test_filter_checklist_wkflvl2_name_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        wkflvl1_1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wkflvl1_2 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wkflvl2_1 = factories.WorkflowLevel2(
            name='WorkflowLevel2 A', workflowlevel1=wkflvl1_1)
        wkflvl2_2 = factories.WorkflowLevel2(
            name='WorkflowLevel2 B', workflowlevel1=wkflvl1_2)
        checklist1 = factories.Checklist(
            name='Checklist A', workflowlevel2=wkflvl2_1)
        factories.Checklist(
            name='Checklist B', workflowlevel2=wkflvl2_2)

        request = self.factory.get(
            '/api/checklist'
            '/?workflowlevel2__name=%s'
            % wkflvl2_1.name)
        request.user = self.tola_user.user
        view = ChecklistViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], checklist1.name)

    def test_filter_checklist_owner_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        another_user = factories.User(first_name='Johnn', last_name='Lennon')
        another_tola = factories.TolaUser(user=another_user)
        wkflvl1_1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wkflvl1_2 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wkflvl2_1 = factories.WorkflowLevel2(
            name='WorkflowLevel2 A', workflowlevel1=wkflvl1_1)
        wkflvl2_2 = factories.WorkflowLevel2(
            name='WorkflowLevel2 B', workflowlevel1=wkflvl1_2)
        checklist1 = factories.Checklist(
            name='Checklist A', owner=self.tola_user, workflowlevel2=wkflvl2_1)
        factories.Checklist(
            name='Checklist B', owner=another_tola, workflowlevel2=wkflvl2_2)

        request = self.factory.get(
            '/api/checklist'
            '/?owner=%s'
            % self.tola_user.pk)
        request.user = self.tola_user.user
        view = ChecklistViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], checklist1.name)

