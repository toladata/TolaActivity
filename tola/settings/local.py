"""Development settings and globals."""
import os, yaml

from base import *

def read_yaml(path):
    with open(path) as f:
        data = yaml.load(f)
    return data

SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.abspath(os.path.join(SETTINGS_DIR,
                                          os.pardir,
                                          os.pardir,
                                          'config'))
app_settings = read_yaml(os.path.join(CONFIG_DIR, './settings.secret.yml'))

# MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = app_settings['ADMINS']
# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = app_settings['ADMINS']

# ALLOWED HOSTS
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = app_settings['ALLOWED_HOSTS']

# CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = app_settings['CACHES']

# DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = app_settings['DATABASES']

# DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = True

# EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = app_settings['EMAIL_BACKEND']
EMAIL_FILE_PATH = app_settings['EMAIL_FILE_PATH']

# GOOGLE CLIENT CONFIG
GOOGLE_CLIENT_ID = app_settings['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = app_settings['GOOGLE_CLIENT_SECRET']
GOOGLE_STEP2_URI = app_settings['GOOGLE_STEP2_URI']

# SOCIAL GOOGLE AUTH
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = app_settings['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = app_settings['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = app_settings['SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS']

# TOLA TABLES AUTH
TOLA_TABLES_TOKEN = app_settings['TOLA_TABLES_TOKEN']
TOLA_TABLES_USER = app_settings['TOLA_TABLES_USER']

# LOCAL APPS DEPENDING ON SERVER DEBUG FOR DEV BOXES,
# REPORT BUILDER FOR REPORT SERVER
DEV_APPS = app_settings['DEV_APPS']

INSTALLED_APPS = INSTALLED_APPS + tuple(DEV_APPS)

# If report server then limit navigation and allow access to public dashboards
REPORT_SERVER = False
OFFLINE_MODE = True
NON_LDAP = True
