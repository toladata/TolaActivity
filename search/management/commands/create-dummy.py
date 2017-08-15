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

        if model == '_all':
            print("Creating %d models" % (nr))
            try:
                for i in range(0, nr):
                    self.create_workflowmodels()
                    # create_indicators()
            except Exception, e:
                print(e.message)
                print(traceback.format_exc())
        elif model == 'indicator':
            print("Creating %d Indicator models" % (nr))
            try:
                for i in range(0, nr):
                    self.create_indicators()
            except Exception, e:
                print(e.message)
                print(traceback.format_exc())
        elif model == 'random':
            print(self.random_name())
        else:
            print("Option '"+model+"' not supported")

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
        it = mommy.make(
            IndicatorType,
            indicator_type=self.random_name(),
            description=self.random_name(),
            _fill_optional=True
        )
        wf1 = mommy.make(
            WorkflowLevel1,
            name=self.random_name(),
            description=self.random_name(),
            _fill_optional=True
        )
        i = mommy.make(Indicator,
                name=self.random_name(),
                definition=self.random_name(),
                make_m2m=False,
                _quantity=1,
                _fill_optional=True,
                indicator_type=[it],
                workflowlevel1=[wf1]
        )

    def create_workflowmodels(self):
        user = TolaUser.objects.get(employee_number=123)

        c = mommy.make(Country,
                       country=self.random_name(),
                       description=self.random_name(),
                       make_m2m=True,
                       _quantity=1,
                       _fill_optional=True)
        # country="Country %d" % (random.randint(1, 100))

        fund_code = mommy.make(FundCode,
                       name=self.random_name(),
                               make_m2m=True,
                               _quantity=1,
                               _fill_optional=True)

        sector = mommy.make(Sector,
                       sector=self.random_name(),
                            make_m2m=True,
                            _quantity=1,
                            _fill_optional=True)

        sub_sector = mommy.make(Sector,
                       sector=self.random_name(),
                                make_m2m=True,
                                _quantity=1,
                                _fill_optional=True)

        wf1 = mommy.make(WorkflowLevel1,
                       name=self.random_name(),
                       description=self.random_name(5),
                         make_m2m=True,
                         _quantity=1,
                         _fill_optional=True,
                         country=c,
                         fund_code=fund_code,
                         sector=sector,
                         sub_sector=sub_sector,
                         user_access=[user])

        ptype = mommy.make(ProjectType,
                       name=self.random_name(),
                       description=self.random_name(10),
                           make_m2m=True,
                           _quantity=1,
                           _fill_optional=True)

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

        wf2 = mommy.make(WorkflowLevel2,
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