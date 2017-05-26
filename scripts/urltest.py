"""
import json data from API
IMPORTANT!! you must turn off pagination for this to work from a URL and get all
country records
Install module django-extensions
Runs twice via function calls at bottom once
"""
from django.db import connection, transaction
from django.core.urlresolvers import reverse

cursor = connection.cursor()
from os.path import exists
import json
import unicodedata
import sys


def run():
    absolute_url = reverse('api')
    print(absolute_url)

    print "Thats it"