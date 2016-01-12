import unicodedata
import datetime
import urllib2
import json
import base64
import sys

from djangocosign.models import UserProfile, Country
from activitydb.models import Country as ActivityCountry
from django.core.mail import send_mail, mail_admins, mail_managers, EmailMessage
from django.contrib.auth.models import User

#CREATE NEW DATA DICTIONARY OBJECT 
def siloToDict(silo):
    parsed_data = {}
    key_value = 1
    for d in silo:
        label = unicodedata.normalize('NFKD', d.field.name).encode('ascii','ignore')
        value = unicodedata.normalize('NFKD', d.char_store).encode('ascii','ignore')
        row = unicodedata.normalize('NFKD', d.row_number).encode('ascii','ignore')
        parsed_data[key_value] = {label : value}

        key_value += 1

    return parsed_data


def getCountry(user):
        """
        Returns the object the view is displaying.

        """
        # get users country from django cosign module
        user_countries = UserProfile.objects.all().filter(user=user).values('countries')
        # get the country name from django cosign module
        get_cosign_country = Country.objects.all().filter(id__in=user_countries).values('name')
        # get the id from the activitydb model
        get_countries = ActivityCountry.objects.all().filter(country__in=get_cosign_country)

        return get_countries


def getTolaDataSilos(user):
        """
        Returns a list of silos from TolaData that the logged in user has access to

        """
        url="https://tola-data.mercycorps.org/api/silo/?format=json"
        # set url for json feed here
        json_file = urllib2.urlopen(url)

        print "JSON FILE:"
        print json_file.read()

        #load data
        data = json.load(json_file)
        json_file.close()

        for row in data:
            print row
            vars_to_sql = []
            keys_to_sql = []
            for new_key, new_value in row.iteritems():
                try:
                    new_key = new_key.encode('ascii','ignore')
                    new_value = new_value.encode('ascii','ignore')
                except Exception, err:
                    sys.stderr.write('ERROR: %s\n' % str(err))
                print new_key
                print new_value

                if new_value:
                    #country or region related columns only
                    if new_key in ('country','region','iso_code'):
                        #change iso_code to code for DB table
                        if new_key == 'iso_code':
                            new_key = 'code'
                        keys_to_sql.append(new_key)
                        vars_to_sql.append(new_value)
            silos = keys_to_sql + vars_to_sql


        return silos


def emailGroup(country,group,link,subject,message,submiter=None):
        #email incident to admins in each country assoicated with the projects program
        for single_country in country.all():
            country = Country.objects.all().filter(name=single_country)
            getGroupEmails = User.objects.all().filter(groups__name=group,userprofile__country=country).values_list('email', flat=True)
            print getGroupEmails
            email_link = link
            formatted_email = email_link
            subject = str(subject)
            message = str(message) + formatted_email

            to = [str(item) for item in getGroupEmails]
            if submiter:
                to.append(submiter)
            print to

            email = EmailMessage(subject, message, 'systems@mercycorps.org',
                    to)

            email.send()

        mail_admins(subject, message, fail_silently=False)