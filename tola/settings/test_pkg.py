from test import *

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'oauth2_provider',
]

LOCAL_APPS = [
    'formlibrary',
    'indicators',
    'search',
    'tola',
    'workflow',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

TEST_RUNNER = 'tola.pkg_testrunner.PackageTestSuiteRunner'
