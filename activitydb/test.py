from django.test import TestCase
from django.test import RequestFactory
from django.test import Client
from activitydb.models import Program, Country, Province, Village, District, ProjectAgreement, Sector, ProjectComplete, ProjectType, Community, Office, Documentation, Monitor, Benchmarks, TrainingAttendance, Beneficiary, Budget
from activitydb.views import CommunityUpdate

class CommunityTestCase(TestCase):

    fixtures = ['fixtures/country.json','fixtures/province.json','fixtures/district.json','fixtures/district.json','fixtures/profile_type.json']

    def setUp(self):
        new_country = Country.objects.create(country="testcountry")
        new_country.save()
        get_country = Country.objects.get(country="testcountry")
        new_province = Province.objects.create(name="testprovince", country=get_country)
        new_province.save()
        get_province = Province.objects.get(name="testprovince")
        new_office = Office.objects.create(name="testoffice",province=new_province)
        new_office.save()
        get_office = Office.objects.get(name="testoffice")
        new_community = Community.objects.create(name="testcommunity", country=get_country, office=get_office,province=get_province)
        new_community.save()

    def test_community_exists(self):
        """Check for Community object"""
        get_community = Community.objects.get(name="testcommunity")
        self.assertEqual(Community.objects.filter(id=get_community.id).count(), 1)


class AgreementTestCase(TestCase):

    fixtures = ['fixtures/project_type.json','fixtures/sector.json']

    def setUp(self):
        new_country = Country.objects.create(country="testcountry")
        new_country.save()
        get_country = Country.objects.get(country="testcountry")
        new_program = Program.objects.create(name="testprogram")
        new_program.save()
        get_program = Program.objects.get(name="testprogram")
        new_province = Province.objects.create(name="testprovince", country=get_country)
        new_province.save()
        get_province = Province.objects.get(name="testprovince")
        new_office = Office.objects.create(name="testoffice",province=new_province)
        new_office.save()
        get_office = Office.objects.get(name="testoffice")
        new_community = Community.objects.create(name="testcommunity", country=get_country, office=get_office,province=get_province)
        new_community.save()
        get_community = Community.objects.get(name="testcommunity")
        #load from fixtures
        get_project_type = ProjectType.objects.get(id='1')
        get_sector = Sector.objects.get(id='2')
        new_agreement = ProjectAgreement.objects.create(program=get_program, project_name="testproject", project_type=get_project_type,
                                                      activity_code="111222",office=get_office,
                                                      sector=get_sector)
        new_agreement.save()
        new_agreement.community.add(get_community)

        new_benchmarks = Benchmarks.objects.create(percent_complete="1234", percent_cumulative="14",agreement=new_agreement)
        new_benchmarks.save()

        new_budget = Budget.objects.create(contributor="testbudget", description_of_contribution="new_province", proposed_value="24", agreement=new_agreement)
        new_budget.save()

        new_monitor = Monitor.objects.create(responsible_person="testmonitor", frequency="freq", type="24", agreement=new_agreement)
        new_monitor.save()

    def test_agreement_exists(self):
        """Check for Agreement object"""
        get_agreement = ProjectAgreement.objects.get(project_name="testproject")
        self.assertEqual(ProjectAgreement.objects.filter(id=get_agreement.id).count(), 1)

    def test_benchmark_exists(self):
        """Check for Benchmark object"""
        get_benchmark = Benchmarks.objects.get(percent_complete="1234")
        self.assertEqual(Benchmarks.objects.filter(id=get_benchmark.id).count(), 1)

    def test_budget_exists(self):
        """Check for Budget object"""
        get_budget = Budget.objects.get(contributor="testbudget")
        self.assertEqual(Budget.objects.filter(id=get_budget.id).count(), 1)

    def test_monitor_exists(self):
        """Check for Monitor object"""
        get_monitor = Monitor.objects.get(responsible_person="testmonitor")
        self.assertEqual(Monitor.objects.filter(id=get_monitor.id).count(), 1)


class CompleteTestCase(TestCase):

    fixtures = ['fixtures/project_type.json','fixtures/sector.json']

    def setUp(self):
        new_country = Country.objects.create(country="testcountry")
        new_country.save()
        get_country = Country.objects.get(country="testcountry")
        new_program = Program.objects.create(name="testprogram")
        new_program.save()
        get_program = Program.objects.get(name="testprogram")
        new_province = Province.objects.create(name="testprovince", country=get_country)
        new_province.save()
        get_province = Province.objects.get(name="testprovince")
        new_office = Office.objects.create(name="testoffice",province=new_province)
        new_office.save()
        get_office = Office.objects.get(name="testoffice")
        new_community = Community.objects.create(name="testcommunity", country=get_country, office=get_office,province=get_province)
        new_community.save()
        get_community = Community.objects.get(name="testcommunity")
        #load from fixtures
        get_project_type = ProjectType.objects.get(id='1')
        get_sector = Sector.objects.get(id='2')
        new_agreement = ProjectAgreement.objects.create(program=get_program, project_name="testproject", project_type=get_project_type,
                                                      activity_code="111222",office=get_office,
                                                      sector=get_sector)
        new_agreement.save()
        new_agreement.community.add(get_community)
        get_agreement = ProjectAgreement.objects.get(project_name="testproject")
        new_complete = ProjectComplete.objects.create(program=get_program, project_name="testproject",
                                                      activity_code="111222",office=get_office,on_time=True,
                                                      project_agreement=get_agreement)
        new_complete.save()
        new_complete.community.add(get_community)

    def test_complete_exists(self):
        """Check for Complete object"""
        get_complete = ProjectComplete.objects.get(project_name="testproject")
        self.assertEqual(ProjectComplete.objects.filter(id=get_complete.id).count(), 1)


class TrainingAttendanceTestCase(TestCase):

    def setUp(self):
        new_program = Program.objects.create(name="testprogram")
        new_program.save()
        get_program = Program.objects.get(name="testprogram")
        new_training = TrainingAttendance.objects.create(training_name="testtraining", program=get_program,
                                                           implementer = "34",
                                                           reporting_period = "34",
                                                           total_participants = "34",
                                                           location = "34",
                                                           community = "34",
                                                           training_duration = "34",
                                                           start_date = "34",
                                                           end_date = "34",
                                                           trainer_name = "34",
                                                           trainer_contact_num = "34",
                                                           form_filled_by = "34",
                                                           form_filled_by_contact_num = "34",
                                                           total_male = "34",
                                                           total_female = "34",
                                                           total_age_0_14_male = "34",
                                                           total_age_0_14_female = "34",
                                                           total_age_15_24_male = "34",
                                                           total_age_15_24_female = "34",
                                                           total_age_25_59_male = "34"
                                                         )
        new_training.save()

    def test_training_exists(self):
        """Check for Training object"""
        get_training = TrainingAttendance.objects.get(training_name="testtraining")
        self.assertEqual(TrainingAttendance.objects.filter(id=get_training.id).count(), 1)


class BeneficiaryTestCase(TestCase):

    def setUp(self):
        new_program = Program.objects.create(name="testprogram")
        new_program.save()
        get_program = Program.objects.get(name="testprogram")
        new_training = TrainingAttendance.objects.create(training_name="testtraining", program=get_program)
        new_training.save()
        get_training = TrainingAttendance.objects.get(training_name="testtraining")
        new_benny = Beneficiary.objects.create(beneficiary_name="Joe Test", training=get_training, father_name="Mr Test", age="42", gender="male", signature=False,remarks="life")
        new_benny.save()

    def test_beneficiary_exists(self):
        """Check for Benny object"""
        get_benny = Beneficiary.objects.get(beneficiary_name="Joe Test")
        self.assertEqual(Beneficiary.objects.filter(id=get_benny.id).count(), 1)