from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import json
import factories
from feed.views import ObjectiveViewSet
from indicators.models import Objective
from workflow.models import WorkflowLevel1, WorkflowTeam, \
    ROLE_ORGANIZATION_ADMIN, ROLE_PROGRAM_TEAM, ROLE_PROGRAM_ADMIN, \
    ROLE_VIEW_ONLY


class ObjectiveViewTest(TestCase):
    def setUp(self):
        factories.Objective.create_batch(2)
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_list_objective_superuser(self):
        request = self.factory.get('/api/objective/')
        request.user = factories.User.build(is_superuser=True,
                                            is_staff=True)
        view = ObjectiveViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_objective_normaluser(self):
        request = self.factory.get('/api/objective/')
        request.user = self.tola_user.user
        view = ObjectiveViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_objective_normaluser_one_result(self):
        request = self.factory.get('/api/objective/')
        wflvl1 = WorkflowLevel1.objects.create(
            name='WorkflowLevel1', organization=self.tola_user.organization)
        WorkflowTeam.objects.create(workflow_user=self.tola_user,
                                    workflowlevel1=wflvl1)
        factories.Objective(workflowlevel1=wflvl1)

        request.user = self.tola_user.user
        view = ObjectiveViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_create_objective_org_admin(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.post('/api/objective/')
        wflvl1 = factories.WorkflowLevel1()
        wflvl1_url = reverse('workflowlevel1-detail', kwargs={'pk': wflvl1.id},
                             request=request)

        data = {'name': 'Macht Deutschland wieder gesund',
                'workflowlevel1': wflvl1_url}
        request = self.factory.post('/api/objective/', data)
        request.user = self.tola_user.user
        view = ObjectiveViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'],
                         u'Macht Deutschland wieder gesund')

    def test_create_objective_program_admin(self):
        request = self.factory.post('/api/objective/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail', kwargs={'pk': wflvl1.id},
                             request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        data = {'name': 'Macht Deutschland wieder gesund',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/objective/', data)
        request.user = self.tola_user.user
        view = ObjectiveViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'],
                         u'Macht Deutschland wieder gesund')

    def test_create_objective_program_admin_json(self):
        request = self.factory.post('/api/objective/')
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wflvl1_url = reverse('workflowlevel1-detail', kwargs={'pk': wflvl1.id},
                             request=request)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        data = {'name': 'Macht Deutschland wieder gesund',
                'workflowlevel1': wflvl1_url}

        request = self.factory.post('/api/objective/', json.dumps(data),
                                    content_type='application/json')
        request.user = self.tola_user.user
        view = ObjectiveViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'],
                         u'Macht Deutschland wieder gesund')

    def test_delete_objective_non_existing(self):
        request = self.factory.delete('/api/objective/')
        request.user = self.tola_user.user
        view = ObjectiveViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=288)
        self.assertEquals(response.status_code, 404)

    def test_delete_objective_superuser(self):
        self.tola_user.user.is_superuser = True
        self.tola_user.user.is_staff = True
        self.tola_user.user.save()

        objective = factories.Objective()
        request = self.factory.delete('/api/objective/')
        request.user = self.tola_user.user
        view = ObjectiveViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=objective.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Objective.DoesNotExist,
            Objective.objects.get, pk=objective.pk)

    def test_delete_objective_org_admin(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        objective = factories.Objective(workflowlevel1=wflvl1)
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.delete('/api/objective/')
        request.user = self.tola_user.user
        view = ObjectiveViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=objective.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Objective.DoesNotExist,
            Objective.objects.get, pk=objective.pk)

    def test_delete_objective_diff_org_org_admin(self):
        another_org = factories.Organization(name='Another Org')
        wflvl1 = factories.WorkflowLevel1(organization=another_org)
        objective = factories.Objective(workflowlevel1=wflvl1)
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.delete('/api/objective/')
        request.user = self.tola_user.user
        view = ObjectiveViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=objective.pk)
        self.assertEquals(response.status_code, 403)
        Objective.objects.get(pk=objective.pk)

    def test_delete_objective_program_admin(self):
        wflvl1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        objective = factories.Objective(workflowlevel1=wflvl1)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=factories.Group(name=ROLE_PROGRAM_ADMIN)
        )

        request = self.factory.delete('/api/objective/')
        request.user = self.tola_user.user
        view = ObjectiveViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=objective.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Objective.DoesNotExist,
            Objective.objects.get, pk=objective.pk)

    def test_delete_objective_diff_org_program_admin(self):
        another_org = factories.Organization(name='Another Org')
        wflvl1 = factories.WorkflowLevel1(organization=another_org)
        objective = factories.Objective(workflowlevel1=wflvl1)
        group_org_admin = factories.Group(name=ROLE_PROGRAM_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.delete('/api/objective/')
        request.user = self.tola_user.user
        view = ObjectiveViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=objective.pk)
        self.assertEquals(response.status_code, 403)
        Objective.objects.get(pk=objective.pk)

    def test_delete_objective_normal_user(self):
        objective = factories.Objective()

        request = self.factory.delete('/api/objective/')
        request.user = self.tola_user.user
        view = ObjectiveViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=objective.pk)
        self.assertEquals(response.status_code, 403)
        Objective.objects.get(pk=objective.pk)


class ObjectiveFilterViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_filter_indicator_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        another_org = factories.Organization(name='Another Org')
        wflvl1_1 = WorkflowLevel1.objects.create(
            name='WorkflowLevel1', organization=self.tola_user.organization)
        wflvl1_2 = WorkflowLevel1.objects.create(
            name='WorkflowLevel1', organization=another_org)
        objective1 = factories.Objective(workflowlevel1=wflvl1_1)
        factories.Objective(name='20% increase in incomes',
                            workflowlevel1=wflvl1_2)

        request = self.factory.get(
            '/api/objective/?workflowlevel1__organization__id=%s' %
            self.tola_user.organization.pk)
        request.user = self.tola_user.user
        view = ObjectiveViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], objective1.name)
