import unicodedata
import json
import sys
import requests

from workflow.models import Country, TolaUser, TolaSites
from django.contrib.auth.models import User
from django.core.mail import send_mail, mail_admins, mail_managers, EmailMessage
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test


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
        user_countries = TolaUser.objects.all().filter(user__id=user.id).values('countries')

        get_countries = Country.objects.all().filter(id__in=user_countries)

        return get_countries


def emailGroup(country,group,link,subject,message,submiter=None):
        #email incident to admins in each country assoicated with the projects program
        for single_country in country.all():
            country = Country.objects.all().filter(country=single_country)
            getGroupEmails = User.objects.all().filter(tola_user=group,tola_user__country=country).values_list('email', flat=True)
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


def get_table(url,data=None):
    """
    Get table data from a Silo.  First get the Data url from the silo details
    then get data and return it
    :param url: URL to silo meta detail info
    :return: json dump of table data
    """
    token = TolaSites.objects.get(site_id=1)
    if token.tola_tables_token:
        headers = {'content-type': 'application/json',
               'Authorization': 'Token ' + token.tola_tables_token }
    else:
        headers = {'content-type': 'application/json'}
        print "Token Not Found"

    response = requests.get(url,headers=headers, verify=True)
    if data:
        data = json.loads(response.content['data'])
    else:
        data = json.loads(response.content)
    return data


def user_to_tola(backend, user, response, *args, **kwargs):

    # Add a google auth user to the tola profile
    default_country = Country.objects.first()
    userprofile, created = TolaUser.objects.get_or_create(
        user = user)

    userprofile.country = default_country

    userprofile.name = response.get('displayName')

    userprofile.email = response.get('emails["value"]')

    userprofile.save()
    #add user to country permissions table
    userprofile.countries.add(default_country)


def group_excluded(*group_names, **url):
    # If user is in the group passed in permission denied
    def in_groups(u):
        if u.is_authenticated():
            if not bool(u.groups.filter(name__in=group_names)):
                return True
            raise PermissionDenied
        return False
    return user_passes_test(in_groups)


def group_required(*group_names, **url):
    # Requires user membership in at least one of the groups passed in.
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
            raise PermissionDenied
        return False
    return user_passes_test(in_groups)
