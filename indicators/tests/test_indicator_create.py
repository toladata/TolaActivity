from unittest import skip

from django.test import TestCase, RequestFactory

from TolaActivity.factories import UserFactory
from factories.indicators_models import (IndicatorTypeFactory,
                                         ExternalServiceFactory)
from factories.workflow_models import (CountryFactory, ProgramFactory,
                                       TolaUserFactory)
from indicators.views import indicator_create


class IndicatorCreateFunctionTests(TestCase):

    def setUp(self):
        self.user = UserFactory(first_name="Indicator", last_name="CreateTest")
        self.tola_user = TolaUserFactory(user=self.user)
        self.request_factory = RequestFactory()
        self.indicator_type = IndicatorTypeFactory()
        self.country = self.tola_user.country
        self.program = ProgramFactory()

    @skip("Skipping for now switching tasks")
    def test_get(self):
        """It should just return an empty form for us to fillout"""
        path = '/indicator_create/{0}'.format(self.program.id)
        request = self.request_factory.get(path=path)
        request.user = self.user
        result = indicator_create(request, id=self.program.id)

        print result.content