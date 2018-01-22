from django.test import TestCase
from rest_framework.test import APIRequestFactory

import factories
from feed.views import ProgramIndicatorReadOnlyViewSet


class ProgramIndicatorReadOnlyListViewsTest(TestCase):
    def setUp(self):
        factories.Organization(id=1)
        self.factory = APIRequestFactory()
        self.tola_user = factories.TolaUser()

    def test_list_program_indicator(self):
        wflvl1 = factories.WorkflowLevel1()
        level = factories.Level(organization=self.tola_user.organization)
        indicator = factories.Indicator(workflowlevel1=[wflvl1], level=level)
        indicator_types = factories.IndicatorType.create_batch(2)
        indicator.indicator_type.add(*indicator_types)
        factories.Indicator(workflowlevel1=[wflvl1])

        request = self.factory.get('')
        request.user = self.tola_user.user
        view = ProgramIndicatorReadOnlyViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)
