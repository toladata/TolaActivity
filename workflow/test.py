from django.test import TestCase
from workflow.models import Organization, WorkflowLevel1, Country, Province, WorkflowLevel2, Sector, ProjectType, \
    SiteProfile, Office, WorkflowLevel3, Budget


class SiteProfileTestCase(TestCase):

    fixtures = ['fixtures/organization.json','fixtures/profiletypes.json']

    def setUp(self):
        new_organization = Organization.objects.create(name="tola")
        new_organization.save()
        get_organization = Organization.objects.get(name="tola")
        new_country = Country.objects.create(country="testcountry", organization=get_organization)
        new_country.save()
        get_country = Country.objects.get(country="testcountry")
        new_province = Province.objects.create(name="testprovince", country=get_country)
        new_province.save()
        get_province = Province.objects.get(name="testprovince")
        new_office = Office.objects.create(name="testoffice", country=new_country)
        new_office.save()
        get_office = Office.objects.get(name="testoffice")
        new_community = SiteProfile.objects.create(name="testcommunity", country=get_country, office=get_office,province=get_province)
        new_community.save()

    def test_community_exists(self):
        """Check for SiteProfile Object"""
        get_community = SiteProfile.objects.get(name="testcommunity")
        self.assertEqual(SiteProfile.objects.filter(id=get_community.id).count(), 1)


class AgreementTestCase(TestCase):

    fixtures = ['fixtures/projecttype.json','fixtures/sectors.json']

    def setUp(self):
        new_organization = Organization.objects.create(name="tola")
        new_organization.save()
        get_organization = Organization.objects.get(name="tola")
        new_country = Country.objects.create(country="testcountry", organization=get_organization)
        new_country.save()
        get_country = Country.objects.get(country="testcountry")
        new_program = WorkflowLevel1.objects.create(name="testprogram")
        new_program.save()
        new_program.country.add(get_country)
        get_program = WorkflowLevel1.objects.get(name="testprogram")
        new_province = Province.objects.create(name="testprovince", country=get_country)
        new_province.save()
        get_province = Province.objects.get(name="testprovince")
        new_office = Office.objects.create(name="testoffice", country=get_country)
        new_office.save()
        get_office = Office.objects.get(name="testoffice")
        new_community = SiteProfile.objects.create(name="testcommunity", country=get_country, office=get_office,province=get_province)
        new_community.save()
        get_community = SiteProfile.objects.get(name="testcommunity")
        #load from fixtures
        get_project_type = ProjectType.objects.get(id='1')
        get_sector = Sector.objects.get(id='2')
        new_agreement = WorkflowLevel2.objects.create(workflowlevel1=get_program, project_name="testproject", project_type=get_project_type,
                                                      activity_code="111222",office=get_office,
                                                      sector=get_sector, on_time=True, community_handover=False)
        new_agreement.save()
        new_agreement.site.add(get_community)

        new_benchmarks = WorkflowLevel3.objects.create(percent_complete="1234", percent_cumulative="14",workflowlevel2=new_agreement)
        new_benchmarks.save()

        new_budget = Budget.objects.create(contributor="testbudget", description_of_contribution="new_province", proposed_value="24", workflowlevel2=new_agreement)
        new_budget.save()

    def test_agreement_exists(self):
        """Check for Agreement object"""
        get_agreement = WorkflowLevel2.objects.get(project_name="testproject")
        self.assertEqual(WorkflowLevel2.objects.filter(id=get_agreement.id).count(), 1)

    def test_benchmark_exists(self):
        """Check for Benchmark object"""
        get_benchmark = WorkflowLevel3.objects.get(percent_complete="1234")
        self.assertEqual(WorkflowLevel3.objects.filter(id=get_benchmark.id).count(), 1)

    def test_budget_exists(self):
        """Check for Budget object"""
        get_budget = Budget.objects.get(contributor="testbudget")
        self.assertEqual(Budget.objects.filter(id=get_budget.id).count(), 1)


class CompleteTestCase(TestCase):

    fixtures = ['fixtures/projecttype.json','fixtures/sectors.json']

    def setUp(self):
        new_organization = Organization.objects.create(name="tola")
        new_organization.save()
        get_organization = Organization.objects.get(name="tola")
        new_country = Country.objects.create(country="testcountry", organization=get_organization)
        new_country.save()
        get_country = Country.objects.get(country="testcountry")
        new_program = WorkflowLevel1.objects.create(name="testprogram")
        new_program.save()
        new_program.country.add(get_country)
        get_program = WorkflowLevel1.objects.get(name="testprogram")
        new_province = Province.objects.create(name="testprovince", country=get_country)
        new_province.save()
        get_province = Province.objects.get(name="testprovince")
        new_office = Office.objects.create(name="testoffice", country=get_country)
        new_office.save()
        get_office = Office.objects.get(name="testoffice")
        new_community = SiteProfile.objects.create(name="testcommunity", country=get_country, office=get_office,province=get_province)
        new_community.save()
        get_community = SiteProfile.objects.get(name="testcommunity")
        #load from fixtures
        get_project_type = ProjectType.objects.get(id='1')
        get_sector = Sector.objects.get(id='2')
        new_agreement = WorkflowLevel2.objects.create(workflowlevel1=get_program, project_name="testproject", project_type=get_project_type,
                                                        activity_code="111222", office=get_office,
                                                        sector=get_sector, on_time=True, community_handover=False)
        new_agreement.save()
        new_agreement.site.add(get_community)
        get_agreement = WorkflowLevel2.objects.get(project_name="testproject")
        new_complete = WorkflowLevel2.objects.create(workflowlevel1=get_program, project_name="testproject",
                                                      activity_code="111222",office=get_office,on_time=True,
                                                       community_handover=1)
        new_complete.save()

    def test_complete_exists(self):
        """Check for Complete object"""
        # get_complete = WorkflowLevel2.objects.get(project_name="testproject")
        self.assertEqual(WorkflowLevel2.objects.count(), 2)

