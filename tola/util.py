import unicodedata
import urllib2
import json
import sys

from activitydb.models import Country, TolaUser, TolaSites
from django.contrib.auth.models import User
from django.core.mail import send_mail, mail_admins, mail_managers, EmailMessage


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


def getTolaDataSilos(user):
        """
        Returns a list of silos from TolaData that the logged in user has access to
        """
        token = TolaSites.objects.get(site_id=1).value("tola_tables_token")
        url="https://tola-data.mercycorps.org/api/silo/?format=json"
        headers = {'content-type': 'application/json',
               'Authorization': 'Token ' + token}

        response = requests.get(url,headers=headers, verify=False)
        # set url for json feed here
        json_file = response

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
            country = Country.objects.all().filter(country=single_country)
            getGroupEmails = User.objects.all().filter(groups__name=group,tola_user__country=country).values_list('email', flat=True)
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


def import_table(request):
    """
    import collected data from Tola Tables
    """
    owner = request.user
    service = ExternalService.objects.get(name="TolaTables")

    #add filter to get just the users tables only
    user_filter_url = service.feed_url + "&owner__username=" + str(owner)
    #public_filter_url = service.feed_url + "&public=True"
    #shared_filter_url = service.feed_url + "&shared__username=" + str(owner)

    token = TolaSites.objects.get(site_id=1)
    if token.tola_tables_token:
        headers = {'content-type': 'application/json',
               'Authorization': 'Token ' + token.tola_tables_token}
    else:
        headers = {'content-type': 'application/json'}
        print "Token Not Found"

    response = requests.get(user_filter_url,headers=headers, verify=False)
    user_json = json.loads(response.content)

    data = user_json

    #debug the json data string uncomment dump and print
    #data2 = json.dumps(data) # json formatted string
    #print data2

    if request.method == 'POST':
        id = request.POST['service_table']
        filter_url = service.feed_url + "&id=" + id
        response = requests.get(filter_url)
        get_json = json.loads(response.content)
        data = get_json
        for item in data['results']:
            name = item['name']
            url = item['data']
            remote_owner = item['owner']['username']

        check_for_existence = TolaTable.objects.all().filter(name=name,owner=owner)
        if check_for_existence:
            result = "error"
        else:
            create_table = TolaTable.objects.create(name=name,owner=owner,remote_owner=remote_owner,table_id=id,url=url)
            create_table.save()
            result = "success"

        #send result back as json
        message = result
        return json.dumps(message)


def user_to_tola(backend, user, response, *args, **kwargs):

    # Add a google auth user to the tola profile
    default_country = Country.objects.get(id=1)
    userprofile, created = TolaUser.objects.get_or_create(
        user = user)

    userprofile.country = default_country

    userprofile.name = response.get('displayName')

    userprofile.email = response.get('emails["value"]')

    userprofile.save()
    #add user to country permissions table
    userprofile.countries.add(default_country)