import random

from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

from indicators.models import Indicator, IndicatorType
from workflow.models import *
import traceback


def run():
    n = 1000
    try:
        for i in range(0,n):
            create_workflowmodels()
            #create_indicators()
    except Exception, e:
        print(e.message)
        print(traceback.format_exc())


def create_indicators():
    it = mommy.make(IndicatorType, _fill_optional=True)
    wf1 = mommy.make(WorkflowLevel1, _fill_optional=True)
    i = mommy.make(Indicator,
                      make_m2m=True,
                      _quantity=1,
                      _fill_optional=True,
                      indicator_type=[it],
                      workflowlevel1=[wf1])


def create_workflowmodels():
    user = TolaUser.objects.get(employee_number=123)

    c = mommy.make(Country,
                   make_m2m=True,
                   _quantity=1,
                   _fill_optional=True,
                   country="Country %d"% (random.randint(1, 100)))

    fund_code = mommy.make(FundCode,
                      make_m2m=True,
                      _quantity=1,
                      _fill_optional=True)

    sector = mommy.make(Sector,
                      make_m2m=True,
                      _quantity=1,
                      _fill_optional=True)

    sub_sector = mommy.make(Sector,
                      make_m2m=True,
                      _quantity=1,
                      _fill_optional=True)

    wf1 = mommy.make(WorkflowLevel1,
                      make_m2m=True,
                      _quantity=1,
                      _fill_optional=True,
                     country=c,
                     fund_code=fund_code,
                     sector=sector,
                     sub_sector=sub_sector,
                     user_access=[user])

    ptype = mommy.make(ProjectType,
                      make_m2m=True,
                      _quantity=1,
                      _fill_optional=True)

    site = mommy.make(SiteProfile,
                      make_m2m=True,
                      _quantity=1,
                      _fill_optional=True,
                      approved_by=user,
                      filled_by=user,
                      location_verified_by=user)

    """stakeholder = mommy.make(Stakeholder,
                      make_m2m=True,
                      _quantity=1,
                      _fill_optional=True,
                     country=c,
                     sector=sector,
                             )"""

    wf2 = mommy.make(WorkflowLevel2,
                      make_m2m=True,
                      _quantity=1,
                      _fill_optional=True,
                      workflowlevel1=wf1[0],
                     project_type=ptype[0],
                     site=site,
                     sector=sector[0],
                     #stakeholder=stakeholder
                     )