from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.reverse import reverse

import factories
from feed.views import BudgetViewSet
from workflow.models import Budget


class BudgetListViewTest(TestCase):
    def setUp(self):
        wflvl1 = factories.WorkflowLevel1()
        wflvl2 = factories.WorkflowLevel2(name='WorkflowLevel2',
                                          workflowlevel1=wflvl1)
        factories.Budget.create_batch(2, workflowlevel2=wflvl2)

        factory = APIRequestFactory()
        self.request = factory.get('/api/budget/')

    def test_list_budget_superuser(self):
        self.request.user = factories.User.build(is_superuser=True,
                                                 is_staff=True)
        view = BudgetViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_budget_normaluser(self):
        tola_user = factories.TolaUser()
        self.request.user = tola_user.user
        view = BudgetViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_budget_normaluser_one_result(self):
        tola_user = factories.TolaUser()
        wflvl1 = factories.WorkflowLevel1(
            name='WorkflowLevel1', organization=tola_user.organization)
        wflvl2 = factories.WorkflowLevel2(
            name='WorkflowLevel2', workflowlevel1=wflvl1)
        factories.Budget(workflowlevel2=wflvl2)

        self.request.user = tola_user.user
        view = BudgetViewSet.as_view({'get': 'list'})
        response = view(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class BudgetCreateViewTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()
        self.factory = APIRequestFactory()

    def test_create_budget(self):
        request = self.factory.post('/api/budget/')

        wflvl1 = factories.WorkflowLevel1(
            name='WorkflowLevel1', organization=self.tola_user.organization)
        wflvl2 = factories.WorkflowLevel2(
            name='WorkflowLevel2', actual_cost=0, total_estimated_budget=0,
            workflowlevel1=wflvl1)
        wflvl2_url = reverse('workflowlevel2-detail',
                             kwargs={'pk': wflvl2.id},
                             request=request)
        user_url = reverse('user-detail', kwargs={'pk': self.tola_user.user.id},
                           request=request)

        data = {'proposed_value': 5678,
                'actual_value': 1234,
                'workflowlevel2': wflvl2_url}
        request = self.factory.post('/api/budget/', data)
        request.user = self.tola_user.user
        view = BudgetViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['proposed_value'],
                         data['proposed_value'])
        self.assertEqual(response.data['actual_value'], data['actual_value'])
        self.assertEqual(response.data['created_by'], user_url)

        # Check WorkflowLevel2
        budget = Budget.objects.get(pk=response.data['id'])
        wkfl2 = budget.workflowlevel2
        self.assertEquals(wkfl2.total_estimated_budget, data['proposed_value'])
        self.assertEquals(wkfl2.actual_cost, data['actual_value'])

    def test_create_budget_without_wkfl2(self):
        request = self.factory.post('/api/budget/')

        user_url = reverse('user-detail', kwargs={'pk': self.tola_user.user.id},
                           request=request)

        data = {'proposed_value': 5678,
                'actual_value': 1234}
        request = self.factory.post('/api/budget/', data)
        request.user = self.tola_user.user
        view = BudgetViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['proposed_value'],
                         data['proposed_value'])
        self.assertEqual(response.data['actual_value'], data['actual_value'])
        self.assertEqual(response.data['created_by'], user_url)


class BudgetUpdateViewTest(TestCase):
    def setUp(self):
        self.tola_user = factories.TolaUser()
        self.factory = APIRequestFactory()

    def test_update_budget(self):
        wflvl1 = factories.WorkflowLevel1(
            name='WorkflowLevel1', organization=self.tola_user.organization)
        wflvl2 = factories.WorkflowLevel2(
            name='WorkflowLevel2', actual_cost=0, total_estimated_budget=0,
            workflowlevel1=wflvl1)
        budget = factories.Budget(workflowlevel2=wflvl2)

        data = {'proposed_value': 5678,
                'actual_value': 1234}
        request = self.factory.post('/api/budget/', data)
        request.user = self.tola_user.user
        view = BudgetViewSet.as_view({'post': 'update'})
        response = view(request, pk=budget.pk)

        budget = Budget.objects.get(pk=response.data['id'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['proposed_value'], budget.proposed_value)
        self.assertEqual(response.data['actual_value'], budget.actual_value)

        # Check WorkflowLevel2
        wkfl2 = budget.workflowlevel2
        self.assertEquals(wkfl2.total_estimated_budget, data['proposed_value'])
        self.assertEquals(wkfl2.actual_cost, data['actual_value'])

    def test_update_budget_without_wkfl2(self):
        budget = factories.Budget()

        data = {'proposed_value': 5678,
                'actual_value': 1234}
        request = self.factory.post('/api/budget/', data)
        request.user = self.tola_user.user
        view = BudgetViewSet.as_view({'post': 'create'})
        response = view(request, pk=budget.pk)

        budget = Budget.objects.get(pk=response.data['id'])
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['proposed_value'], budget.proposed_value)
        self.assertEqual(response.data['actual_value'], budget.actual_value)


class BudgetFilterViewTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_filter_budget_org_superuser(self):
        self.tola_user.user.is_staff = True
        self.tola_user.user.is_superuser = True
        self.tola_user.user.save()

        another_org = factories.Organization(name='Another Org')
        wkflvl1_1 = factories.WorkflowLevel1(
            organization=self.tola_user.organization)
        wkflvl1_2 = factories.WorkflowLevel1(organization=another_org)
        wkflvl2_1 = factories.WorkflowLevel2(workflowlevel1=wkflvl1_1)
        wkflvl2_2 = factories.WorkflowLevel2(workflowlevel1=wkflvl1_2)
        budget1 = factories.Budget(workflowlevel2=wkflvl2_1)
        factories.Budget(contributor='Paul McCartney', workflowlevel2=wkflvl2_2)

        request = self.factory.get(
            '/api/budget/?workflowlevel2__workflowlevel1__organization__id'
            '=%s' % self.tola_user.organization.pk)
        request.user = self.tola_user.user
        view = BudgetViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['contributor'], budget1.contributor)
