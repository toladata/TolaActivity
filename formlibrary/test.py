from django.test import TestCase
from workflow.models import WorkflowLevel1, Country, AdminLevelOne, WorkflowLevel2, Sector, SiteProfile, Office
from formlibrary.models import TrainingAttendance, Distribution, Beneficiary
from datetime import datetime


class TrainingAttendanceTestCase(TestCase):

    def setUp(self):
        new_program = WorkflowLevel1.objects.create(name="testprogram")
        new_program.save()
        get_program = WorkflowLevel1.objects.get(name="testprogram")
        new_training = TrainingAttendance.objects.create(training_name="testtraining", workflowlevel1=get_program,
                                                           implementer = "34",
                                                           reporting_period = "34",
                                                           total_participants = "34",
                                                           location = "34",
                                                           community = "34",
                                                           training_duration = "34",
                                                           start_date = "34",
                                                           end_date = "34",
                                                           trainer_name = "34",
                                                         )
        new_training.save()

    def test_training_exists(self):
        """Check for Training object"""
        get_training = TrainingAttendance.objects.get(training_name="testtraining")
        self.assertEqual(TrainingAttendance.objects.filter(id=get_training.id).count(), 1)


class DistributionTestCase(TestCase):

    fixtures = ['fixtures/001_organization.json','fixtures/007_projecttype.json','fixtures/003_sectors.json']

    def setUp(self):
        new_program = WorkflowLevel1.objects.create(name="testprogram")
        new_program.save()
        get_program = WorkflowLevel1.objects.get(name="testprogram")
        new_country = Country.objects.create(country="testcountry")
        new_country.save()
        get_country = Country.objects.get(country="testcountry")
        new_province = AdminLevelOne.objects.create(name="testprovince", country=get_country)
        new_province.save()
        get_province = AdminLevelOne.objects.get(name="testprovince")
        new_office = Office.objects.create(name="testoffice", country=new_country)
        new_office.save()
        get_office = Office.objects.get(name="testoffice")
        #create project agreement -- and load from fixtures
        new_community = SiteProfile.objects.create(name="testcommunity", country=get_country, office=get_office,province=get_province)
        new_community.save()
        get_community = SiteProfile.objects.get(name="testcommunity")
        get_sector = Sector.objects.get(id='2')
        new_agreement = WorkflowLevel2.objects.create(workflowlevel1=get_program, name="testproject",
                                                      office=get_office,
                                                      sector=get_sector, on_time=True, community_handover=False)
        new_agreement.save()
        new_agreement.site.add(get_community)
        get_agreement = WorkflowLevel2.objects.get(name="testproject")
        new_distribution = Distribution.objects.create(distribution_name="testdistribution", workflowlevel1=get_program,
                                                            workflowlevel2=get_agreement,
                                                            office_code=get_office,
                                                            distribution_implementer = "34",
                                                            reporting_period = "34",
                                                            province=get_province,
                                                            total_beneficiaries_received_input = "34",
                                                            distribution_location = "testlocation",
                                                            input_type_distributed = "testinputtype",
                                                            distributor_name_and_affiliation = "testdistributorperson",
                                                            distributor_contact_number = "1-dis-tri-bute",
                                                         )
        new_distribution.save()

    def test_distribution_exists(self):
        """Check for Distribution object"""
        get_distribution = Distribution.objects.get(distribution_name="testdistribution")
        self.assertEqual(Distribution.objects.filter(id=get_distribution.id).count(), 1)


class BeneficiaryTestCase(TestCase):

    def setUp(self):
        new_program = WorkflowLevel1.objects.create(name="testprogram")
        new_program.save()
        get_program = WorkflowLevel1.objects.get(name="testprogram")
        new_training = TrainingAttendance.objects.create(training_name="testtraining", workflowlevel1=get_program)
        new_training.save()
        get_training = TrainingAttendance.objects.get(training_name="testtraining")
        new_benny = Beneficiary.objects.create(beneficiary_name="Joe Test", father_name="Mr Test", age="42", gender="male", signature=False,remarks="life")
        new_benny.training.add(new_training)
        new_benny.save()

    def test_beneficiary_exists(self):
        """Check for Benny object"""
        get_benny = Beneficiary.objects.get(beneficiary_name="Joe Test")
        self.assertEqual(Beneficiary.objects.filter(id=get_benny.id).count(), 1)
