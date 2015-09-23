"""
import json data from API
IMPORTANT!! you must turn off pagination for this to work from a URL and get all
country records
Install module django-extensions
Runs twice via function calls at bottom once
"""
from django.db import connection, transaction

cursor = connection.cursor()
from os.path import exists
import csv
import unicodedata
import sys
import urllib2
from datetime import date
from activitydb.models import Country, Province, District

def run():
    print "Uploading JSON data"

type = "Program"
program_country = 1


def getAllData():

    with open('fixtures/dist_prov.csv', 'rb') as csvfile:
        country = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in country:
            column_num = 0
            new_district = ""
            for column in row:
                if column_num == 0:
                    print "new_district="
                    new_district = column.replace('\n', ' ')
                    print new_district
                else:
                    print "query for province="
                    print column
                    getProvince = Province.objects.get(name=column, country=1)
                    if getProvince:
                        new_dist = District(name=new_district, province=getProvince)
                        new_dist.save()
                    else:
                        new_prov = Province(name=column, country=1)
                        new_prov.save()
                        new_dist = District(name=new_district, province=getProvince)
                        new_dist.save()

                column_num = 1






#query to mysql database after parsing json data
def saveDistrict(keys_to_sql, vars_to_sql):
    #save the original keys list for update in case we need to run that
    save_keys = keys_to_sql

    query = "INSERT INTO activitydb_country (country,code) VALUES ('%s','%s')" % (vars_to_sql[0], vars_to_sql[1])
    print query

    try:
        cursor.execute(query)
        transaction.commit()
    except Exception, err:
        sys.stderr.write('ERROR: %s\n' % str(err))
        column = save_keys[1]
        value = 1
        country = vars_to_sql[0]
        if type == "country":
            query_update = "UPDATE activitydb_country set country = %s where lower(%(type)s) = '%s'" % (
                column, value, country.lower())
        try:
            cursor.execute(query_update)
            transaction.commit()
        except Exception, err:
            sys.stderr.write('ERROR: %s\n' % str(err))
        return 1
pass

getAllData()