from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory

import factories
from feed.views import PortfolioViewSet
from workflow.models import (ROLE_ORGANIZATION_ADMIN, ROLE_PROGRAM_ADMIN,
                             ROLE_PROGRAM_TEAM, ROLE_VIEW_ONLY, Portfolio)


class PortfolioListViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        self.portfolio = factories.Portfolio()

    def test_list_portfolio_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.get('')
        request.user = self.tola_user.user
        view = PortfolioViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]['name'], self.portfolio.name)
        self.assertEqual(response.data[0]['description'],
                         self.portfolio.description)
        organization_url = reverse(
            'organization-detail',
            kwargs={'pk': self.portfolio.organization.pk})
        self.assertIn(organization_url, response.data[0]['organization'])

    def test_list_portfolio_org_admin_same_org(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        self.portfolio.organization = self.tola_user.organization
        self.portfolio.save()

        request = self.factory.get('')
        request.user = self.tola_user.user
        view = PortfolioViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(response.data[0]['name'], self.portfolio.name)
        self.assertEqual(response.data[0]['description'],
                         self.portfolio.description)
        organization_url = reverse(
            'organization-detail',
            kwargs={'pk': self.tola_user.organization.pk})
        self.assertIn(organization_url, response.data[0]['organization'])

    def test_list_portfolio_org_admin_different_org(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.get('')
        request.user = self.tola_user.user
        view = PortfolioViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_portfolio_program_admin(self):
        factories.WorkflowTeam(
            workflow_user=self.tola_user,
            workflowlevel1=factories.WorkflowLevel1(
                organization=self.tola_user.organization),
            role=factories.Group(name=ROLE_PROGRAM_ADMIN))

        self.portfolio.organization = self.tola_user.organization
        self.portfolio.save()

        request = self.factory.get('')
        request.user = self.tola_user.user
        view = PortfolioViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_portfolio_program_team(self):
        factories.WorkflowTeam(
            workflow_user=self.tola_user,
            workflowlevel1=factories.WorkflowLevel1(
                organization=self.tola_user.organization),
            role=factories.Group(name=ROLE_PROGRAM_TEAM))

        self.portfolio.organization = self.tola_user.organization
        self.portfolio.save()

        request = self.factory.get('')
        request.user = self.tola_user.user
        view = PortfolioViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_portfolio_view_only(self):
        factories.WorkflowTeam(
            workflow_user=self.tola_user,
            workflowlevel1=factories.WorkflowLevel1(
                organization=self.tola_user.organization),
            role=factories.Group(name=ROLE_VIEW_ONLY))

        self.portfolio.organization = self.tola_user.organization
        self.portfolio.save()

        request = self.factory.get('')
        request.user = self.tola_user.user
        view = PortfolioViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_portfolio_other_user(self):
        self.portfolio.organization = self.tola_user.organization
        self.portfolio.save()

        request = self.factory.get('')
        request.user = self.tola_user.user
        view = PortfolioViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class PortfolioUpdateViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        self.portfolio = factories.Portfolio()

    def test_update_unexisting_portfolio(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.post(None, {})
        request.user = self.tola_user.user
        view = PortfolioViewSet.as_view({'post': 'update'})
        response = view(request, pk=288)
        self.assertEqual(response.status_code, 404)

    def test_update_portfolio_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        data = {'name': 'Some name'}
        request = self.factory.post(None, data)
        request.user = self.tola_user.user
        view = PortfolioViewSet.as_view({'post': 'update'})
        response = view(request, pk=self.portfolio.pk)
        self.assertEqual(response.status_code, 200)

        name = Portfolio.objects.values_list('name', flat=True).get(
            pk=self.portfolio.pk)
        self.assertEqual(name, 'Some name')

    def test_update_portfolio_org_admin_same_org(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        self.portfolio.organization = self.tola_user.organization
        self.portfolio.save()

        data = {'name': 'Some name'}
        request = self.factory.post(None, data)
        request.user = self.tola_user.user
        view = PortfolioViewSet.as_view({'post': 'update'})
        response = view(request, pk=self.portfolio.pk)
        self.assertEqual(response.status_code, 200)

        name = Portfolio.objects.values_list('name', flat=True).get(
            pk=self.portfolio.pk)
        self.assertEqual(name, 'Some name')

    def test_update_portfolio_org_admin_different_org(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        data = {'name': 'Some name'}
        request = self.factory.post(None, data)
        request.user = self.tola_user.user
        view = PortfolioViewSet.as_view({'post': 'update'})
        response = view(request, pk=self.portfolio.pk)
        self.assertEqual(response.status_code, 403)

    def test_update_portfolio_org_admin_other_user(self):
        role_without_benefits = ROLE_PROGRAM_TEAM
        group_org_admin = factories.Group(name=role_without_benefits)
        self.tola_user.user.groups.add(group_org_admin)

        self.portfolio.organization = self.tola_user.organization
        self.portfolio.save()

        data = {'name': 'Some name'}
        request = self.factory.post(None, data)
        request.user = self.tola_user.user
        view = PortfolioViewSet.as_view({'post': 'update'})
        response = view(request, pk=self.portfolio.pk)
        self.assertEqual(response.status_code, 403)


class PortfolioDeleteViewsTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()
        self.portfolio = factories.Portfolio()

    def test_delete_portfolio_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        request = self.factory.delete(None)
        request.user = self.tola_user.user
        view = PortfolioViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.portfolio.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Portfolio.DoesNotExist,
            Portfolio.objects.get, pk=self.portfolio.pk)

    def test_delete_portfolio_org_admin_same_org(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        self.portfolio.organization = self.tola_user.organization
        self.portfolio.save()

        request = self.factory.delete(None)
        request.user = self.tola_user.user
        view = PortfolioViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.portfolio.pk)
        self.assertEquals(response.status_code, 204)
        self.assertRaises(
            Portfolio.DoesNotExist,
            Portfolio.objects.get, pk=self.portfolio.pk)

    def test_delete_portfolio_org_admin_different_org(self):
        group_org_admin = factories.Group(name=ROLE_ORGANIZATION_ADMIN)
        self.tola_user.user.groups.add(group_org_admin)

        request = self.factory.delete(None)
        request.user = self.tola_user.user
        view = PortfolioViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.portfolio.pk)
        self.assertEquals(response.status_code, 403)
        Portfolio.objects.get(pk=self.portfolio.pk)

    def test_delete_portfolio_org_admin_other_user(self):
        role_without_benefits = ROLE_PROGRAM_TEAM
        group_org_admin = factories.Group(name=role_without_benefits)
        self.tola_user.user.groups.add(group_org_admin)

        self.portfolio.organization = self.tola_user.organization
        self.portfolio.save()

        request = self.factory.delete(None)
        request.user = self.tola_user.user
        view = PortfolioViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.portfolio.pk)
        self.assertEquals(response.status_code, 403)
        Portfolio.objects.get(pk=self.portfolio.pk)
