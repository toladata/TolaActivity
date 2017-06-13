


from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

from indicators.models import Indicator, IndicatorType


def run():
    try:
        create_indicators()
    except Exception, e:
        print(e.message)

def create_indicators():
    it = mommy.make(IndicatorType, _fill_optional=True)
    indi = mommy.make(Indicator, make_m2m=True, _quantity=1, _fill_optional=True, indicator_type=[it])