from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import factories
from feed.views import IndicatorViewSet
from indicators.models import Indicator
from workflow.models import (ROLE_ORGANIZATION_ADMIN, WorkflowTeam,
                             ROLE_PROGRAM_ADMIN)


class IndicatorViewTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()
        self.factory = APIRequestFactory()

    def test_create_indicator_superuser(self):
        self.tola_user.user.is_superuser = True
        self.tola_user.user.is_staff = True
        self.tola_user.user.save()

        request = self.factory.post('/api/indicator/')
        wflvl1 = factories.WorkflowLevel1()
        wflvl1_url = reverse('workflowlevel1-detail', kwargs={'pk': wflvl1.id},
                             request=request)
        user_url = reverse('user-detail', kwargs={'pk': self.tola_user.user.id},
                           request=request)

        data = {'name': 'Building resilience in Mali',
                'workflowlevel1': wflvl1_url}

        request = APIRequestFactory().post('/api/indicator/', data)
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], u'Building resilience in Mali')
        self.assertEqual(response.data['created_by'], user_url)

    def test_delete_indicator_non_existing(self):
        request = self.factory.delete('/api/indicator/')
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=288)
        self.assertEquals(response.status_code, 404)

    def test_delete_indicator_superuser(self):
        self.tola_user.user.is_superuser = True
        self.tola_user.user.is_staff = True
        self.tola_user.user.save()

        indicator = factories.Indicator()
        request = self.factory.delete('/api/indicator/')
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=indicator.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Indicator.DoesNotExist,
            Indicator.objects.get, pk=indicator.pk)

    def test_delete_indicator_org_admin(self):
        wflvl1 = factories.WorkflowLevel1()
        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.delete('/api/indicator/')
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=indicator.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Indicator.DoesNotExist,
            Indicator.objects.get, pk=indicator.pk)

    def test_delete_indicator_different_org_admin(self):
        wflvl1 = factories.WorkflowLevel1()
        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        other_organization = factories.Organization(name='Other Org')
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user, partner_org=other_organization,
            role=group_org_admin)

        request = self.factory.delete('/api/indicator/')
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=indicator.pk)
        self.assertEquals(response.status_code, 403)
        Indicator.objects.get(pk=indicator.pk)

    def test_delete_indicator_program_admin(self):
        wflvl1 = factories.WorkflowLevel1()
        indicator = factories.Indicator(workflowlevel1=[wflvl1])
        group_program_admin = factories.Group(name=ROLE_PROGRAM_ADMIN)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=group_program_admin)

        request = self.factory.delete('/api/indicator/')
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=indicator.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Indicator.DoesNotExist,
            Indicator.objects.get, pk=indicator.pk)

    def test_delete_indicator_program_admin_only_one_worflow(self):
        wflvl0 = factories.WorkflowLevel1()
        wflvl1 = factories.WorkflowLevel1()
        indicator = factories.Indicator(workflowlevel1=[wflvl0, wflvl1])
        group_program_admin = factories.Group(name=ROLE_PROGRAM_ADMIN)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1,
            role=group_program_admin)

        request = self.factory.delete('/api/indicator/')
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=indicator.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Indicator.DoesNotExist,
            Indicator.objects.get, pk=indicator.pk)

    def test_delete_indicator_different_program_admin(self):
        wflvl1 = factories.WorkflowLevel1()
        indicator = factories.Indicator(workflowlevel1=[wflvl1])

        wflvl1_other = factories.WorkflowLevel1()
        group_program_admin = factories.Group(name=ROLE_PROGRAM_ADMIN)
        WorkflowTeam.objects.create(
            workflow_user=self.tola_user,
            workflowlevel1=wflvl1_other,
            role=group_program_admin)

        request = self.factory.delete('/api/indicator/')
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=indicator.pk)
        self.assertEquals(response.status_code, 403)
        Indicator.objects.get(pk=indicator.pk)

    def test_delete_indicator_normal_user(self):
        wflvl1 = factories.WorkflowLevel1()
        indicator = factories.Indicator(workflowlevel1=[wflvl1])

        request = self.factory.delete('/api/indicator/')
        request.user = self.tola_user.user
        view = IndicatorViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=indicator.pk)
        self.assertEquals(response.status_code, 403)
        Indicator.objects.get(pk=indicator.pk)
