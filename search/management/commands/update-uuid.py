from django.core.management.base import BaseCommand
import random

from model_mommy import mommy
from model_mommy.recipe import Recipe, foreign_key

from indicators.models import Indicator, IndicatorType
from workflow.models import *
import traceback


class Command(BaseCommand):
    help = "Add unique TolaUser and Organization UUIDS after model update."

    def handle(self, *args, **options):
        count = 0
        users = TolaUser.objects.all()
        for u in users:
            if len(u.tola_user_uuid) == 0:
                u.tola_user_uuid = uuid.uuid4()
                u.save()
                count += 1

        orgs = Organization.objects.all()
        for org in orgs:
            if len(org.organization_uuid) == 0:
                org.organization_uuid = uuid.uuid4()
                org.save()
                count += 1

        print "Updated "+str(count)+" objects"
