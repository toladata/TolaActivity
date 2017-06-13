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
    import os
    print os.environ["TOLA_DB"]
    DATABASES = {
        'default': {
            'ENGINE': os.environ["TOLA_DB_ENGINE"],
            'NAME': os.environ["TOLA_DB_NAME"],
            'USER': os.environ["TOLA_DB_USER"],
            'PASSWORD': os.environ["TOLA_DB_PASS"],
            'HOST': os.environ["TOLA_DB_HOST"],
            'PORT': os.environ["TOLA_DB_PORT"],
        }
    }
    print DATABASES
    print "Thats it"