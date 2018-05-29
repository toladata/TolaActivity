from django.test import TestCase

from formlibrary.models import TrainingAttendance, Distribution, Beneficiary
from workflow.models import (WorkflowLevel1, Country, AdminLevelOne,
                             WorkflowLevel2, Sector, SiteProfile, Office)


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
