from django.core.management.base import BaseCommand
import random

from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

from indicators.models import Indicator, IndicatorType
from workflow.models import *
import traceback


class Command(BaseCommand):
    help = "Create dummy data for tola activity models."

    def add_arguments(self, parser):
        parser.add_argument('model')
        parser.add_argument('number')

    def handle(self, *args, **options):
        model = options['model']
        nr = int(options['number'])

        print("Creating %d models" % (nr))
        try:
            for i in range(0, nr):
                if model == '_all' or model == 'workflows':
                    self.create_workflowmodels()

                if model == '_all' or model == 'indicators':
                    self.create_indicators()

        except Exception, e:
            print(e.message)
            print(traceback.format_exc())

    def random_name(self, words=2):
        rand_word = ''
        with open('search/fixtures/words.txt') as wordfile:
            word_list = wordfile.readlines()
            for i in range(0, words):
                word = word_list[random.randint(0, len(word_list))]
                if i != 0:
                    rand_word = rand_word+' '+word
                else:
                    rand_word = rand_word + word

        rand_word = rand_word.replace('\n','')
        rand_word = rand_word[0].upper()+rand_word[1:]
        return rand_word

    def create_indicators(self):
        its = IndicatorType.objects.all()

        # Select a random IndicatorType from db
        if len(its) > 0:
            it = its[random.randint(0, len(its) - 1)]
        else:
            # if no exists create one
            it = mommy.make(
                IndicatorType,
                indicator_type=self.random_name(),
                description=self.random_name(),
                _fill_optional=True
            )

        wf1s = WorkflowLevel1.objects.all()
        if len(wf1s) > 0:
            wf1 = wf1s[random.randint(0, len(wf1s) - 1)]
        else:
            wf1 = mommy.make(
                WorkflowLevel1,
                name=self.random_name(),
                description=self.random_name(),
                _fill_optional=True
            )

        mommy.make(Indicator,
                name=self.random_name(),
                definition=self.random_name(4),
                number=random.randint(0, 100),
                source=self.random_name(),
                justification=self.random_name(10),
                unit_of_measure=self.random_name(1),
                make_m2m=False,
                _quantity=1,
                _fill_optional=True,
                indicator_type=[it],
                workflowlevel1=[wf1]
        )

    def create_workflowmodels(self):
        user = TolaUser.objects.get(employee_number=123)

        cs = Country.objects.all()
        if len(cs) > 0:
            c = cs[random.randint(0, len(cs) - 1)]
        else:
            c = mommy.make(Country,
                           country=self.random_name(),
                           description=self.random_name(),
                           make_m2m=False,
                           _quantity=1,
                           _fill_optional=True)

        fcs = Country.objects.all()
        if len(fcs) > 0:
            fund_code = fcs[random.randint(0, len(fcs) - 1)]
        else:
            fund_code = mommy.make(FundCode,
                                   name=self.random_name(),
                                   make_m2m=True,
                                   _quantity=1,
                                   _fill_optional=True)

        sectors = Sector.objects.all()
        if len(sectors) > 0:
            sector = sectors[random.randint(0, len(sectors) - 1)]
        else:
            sector = mommy.make(Sector,
                                sector=self.random_name(),
                                make_m2m=True,
                                _quantity=1,
                                _fill_optional=True)

        wf1s = WorkflowLevel1.objects.all()
        if len(wf1s) > 0:
            wf1 = wf1s[random.randint(0, len(wf1s) - 1)]
        else:
            wf1 = mommy.make(WorkflowLevel1,
                             name=self.random_name(),
                             description=self.random_name(5),
                             make_m2m=True,
                             _quantity=1,
                             _fill_optional=True,
                             country=c,
                             fund_code=fund_code,
                             sector=sector,
                             sub_sector=sector,
                             user_access=[user])

        ptypes = ProjectType.objects.all()
        if len(ptypes) > 0:
            ptype = ptypes[random.randint(0, len(ptypes) - 1)]
        else:
            ptype = mommy.make(ProjectType,
                           name=self.random_name(),
                           description=self.random_name(10),
                           make_m2m=True,
                           _quantity=1,
                           _fill_optional=True)

        sites = SiteProfile.objects.all()
        if len(sites) > 0:
            site = sites[random.randint(0, len(sites) - 1)]
        else:
            site = mommy.make(SiteProfile,
                                name=self.random_name(),
                                contact_leader=self.random_name(1),
                                make_m2m=True,
                                _quantity=1,
                                _fill_optional=True)

        """stakeholder = mommy.make(Stakeholder,
                          make_m2m=True,
                          _quantity=1,
                          _fill_optional=True,
                         country=c,
                         sector=sector,
                                 )"""

        mommy.make(WorkflowLevel2,
                         name=self.random_name(),
                         description=self.random_name(20),
                         make_m2m=True,
                         _quantity=1,
                         _fill_optional=True,
                         workflowlevel1=wf1[0],
                         project_type=ptype[0],
                         site=site,
                         sector=sector[0],
                         # stakeholder=stakeholder
                         )