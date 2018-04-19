from django.test import TestCase, RequestFactory

from factories.indicators_models import IndicatorFactory, IndicatorTypeFactory
from factories.django_models import UserFactory
from factories.workflow_models import TolaUserFactory, ProgramFactory
from indicators.views.views_indicators import IndicatorList


class IndicatorListTests(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.user = UserFactory(first_name="Bobby",
                                last_name="Indicator")
        self.user.tola_user = TolaUserFactory(user=self.user)

    def test_get(self):

        program = ProgramFactory(funding_status="Funded")
        program.country.add(self.user.tola_user.country)
        program.save()
        for country in program.country.all():
            self.user.tola_user.countries.add(country)
            self.user.tola_user.save()
        self.user.tola_user.save()
        indicator_type = IndicatorTypeFactory()
        indicator = IndicatorFactory(program=program)
        indicator.indicator_type.add(indicator_type)

        data = {'program': program.id, 'indicator': indicator.id,
                'type': indicator_type.id}
        path = "/indicator_list/{0}/{1}/{2}/".format(program.id, indicator.id,
                                                     indicator_type.id)
        request = self.request_factory.get(path=path, data=data)
        request.user = self.user

        view = IndicatorList.as_view()

        result = view(request, **data)
        print result.content
        self.assertIn(program.name, result.content)
        self.assertIn(indicator_type.indicator_type, result.content.decode('utf-8'))
