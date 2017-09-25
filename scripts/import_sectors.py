"""
import json data from API
IMPORTANT!! you must turn off pagination for this to work from a URL and get all
country records
Install module django-extensions
Runs twice via function calls at bottom once
Syntax: sudo py manage.py runscript import_adminlevels
"""
from django.db import connection

cursor = connection.cursor()
import csv
from workflow.models import Sector, SectorRelated, Organization

def run():
    print "Uploading Sectors"


def getAllData(file_name):
    org = Organization.objects.get(name="TolaData")

    with open(file_name, 'rb') as csvfile:
        sector = csv.reader(csvfile, delimiter=',', quotechar='"')
        print "Sector"
        #check for province and add new ones
        for row in sector:
            column_num = 0
            for column in row:
                if column_num == 1:
                    print "Sector="
                    print column
                    try:
                        Sector.objects.get(sector=column, organization=org)
                    except Sector.DoesNotExist:
                        new_sector = Sector(sector=column, organization=org)
                        new_sector.save()
                    print column
                if column_num == 2:
                    print "Sector="
                    print column
                    try:
                        Sector.objects.get(sector=column)
                    except Sector.DoesNotExist:
                        new_sector = Sector(sector=column, organization=org)
                        new_sector.save()
                    print column
                column_num = column_num + 1

    with open(file_name, 'rb') as csvfile2:
        sector2 = csv.reader(csvfile2, delimiter=',', quotechar='"')
        #check for distrcit and add new one
        delete = Sector.objects.all().delete()
        delete = SectorRelated.objects.all().delete()
        org = Organization.objects.get(name="TolaData")

        for row in sector2:

            sector = ""
            sector_related = ""
            column_num = 0
            for column in row:

                if column_num == 0:
                    sector = column

                if column_num == 1:
                    sector_related = column
                column_num = column_num + 1

                # Add the sector to the sector object
                try:
                    getSector = Sector.objects.get(sector=sector)
                except Sector.DoesNotExist:
                    new_sector = Sector(sector=sector, organization=org)
                    new_sector.save()
                    getSector = Sector.objects.get(sector=sector)

                # add the sub-sector to the sector object
                print sector_related
                try:
                    getSubSector = Sector.objects.get(sector=sector_related)
                except Sector.DoesNotExist:
                    new_sector = Sector(sector=sector_related, organization=org)
                    new_sector.save()
                    getSubSector = Sector.objects.get(sector=sector_related)

                # add sector and sub-sector to the related object
                try:
                    checksub = SectorRelated.objects.filter(sector=getSector, sector_related=getSubSector, organization=org).get()
                except SectorRelated.DoesNotExist:
                    print "adding new sector related"
                    print getSector
                    print getSubSector
                    print "or not"
                    new_related = SectorRelated(sector=getSector, sector_related=getSubSector, organization=org)
                    new_related.save()
                print row



# UNCOMMENT AND UPDATE TO IMPORT
print "IMPORTING Sectors"
file_name = "fixtures/Sector-SubSector.csv"
getAllData(file_name)


