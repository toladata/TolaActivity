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
app_settings = read_yaml(os.path.join(CONFIG_DIR, 'settings.travis.yml'))

# MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = app_settings.get('ADMINS', None)
# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = app_settings.get('ADMINS', None)

# ALLOWED HOSTS
# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = app_settings.get('ALLOWED_HOSTS', None)

# CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = app_settings.get('CACHES', None)

# DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = app_settings.get('DATABASES', None)

# DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = app_settings.get('DEBUG', None)
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug

# EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_USE_TLS = app_settings.get('EMAIL_USE_TLS', None)
EMAIL_HOST = app_settings.get('EMAIL_HOST', None)
EMAIL_PORT = app_settings.get('EMAIL_PORT', None)
EMAIL_HOST_USER = app_settings.get('EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD = app_settings.get('EMAIL_HOST_PASSWORD', None)
DEFAULT_FROM_EMAIL = app_settings.get('DEFAULT_FROM_EMAIL', None)
SERVER_EMAIL = app_settings.get('SERVER_EMAIL', None)
EMAIL_BACKEND = app_settings.get('EMAIL_BACKEND', None)
EMAIL_FILE_PATH = app_settings.get('EMAIL_FILE_PATH', None)

# GOOGLE CLIENT CONFIG
GOOGLE_CLIENT_ID = app_settings.get('GOOGLE_CLIENT_ID', None)
GOOGLE_CLIENT_SECRET = app_settings.get('GOOGLE_CLIENT_SECRET', None)
GOOGLE_STEP2_URI = app_settings.get('GOOGLE_STEP2_URI', None)

# SOCIAL GOOGLE AUTH
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = app_settings.get('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', None)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = app_settings.get('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', None)
SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = app_settings.get('SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS', None)

# TOLA TABLES AUTH
TOLA_TABLES_TOKEN = app_settings.get('TOLA_TABLES_TOKEN', None)
TOLA_TABLES_USER = app_settings.get('TOLA_TABLES_USER', None)

# LOCAL APPS DEPENDING ON SERVER DEBUG FOR DEV BOXES,
# REPORT BUILDER FOR REPORT SERVER
DEV_APPS = app_settings.get('DEV_APPS', None)

INSTALLED_APPS = INSTALLED_APPS #+ tuple(DEV_APPS)

LDAP_LOGIN = app_settings.get('LDAP_LOGIN', None)
LDAP_SERVER = app_settings.get('LDAP_SERVER', None)
LDAP_PASSWORD = app_settings.get('LDAP_PASSWORD', None)
LDAP_USER_GROUP = app_settings.get('LDAP_USER_GROUP', None)
LDAP_ADMIN_GROUP = app_settings.get('LDAP_ADMIN_GROUP', None)

AUTHENTICATION_BACKENDS = app_settings.get('AUTHENTICATION_BACKENDS', None)

# If report server then limit navigation and allow access to public dashboards
REPORT_SERVER = app_settings.get('REPORT_SERVER', None)
OFFLINE_MODE = app_settings.get('OFFLINE_MODE', None)
NON_LDAP = app_settings.get('NON_LDAP', None)

########## EMAIL SETTINGS
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = app_settings.get('EMAIL_HOST_USER', None)
EMAIL_HOST_PASSWORD = app_settings.get('EMAIL_HOST_PASSWORD', None)
DEFAULT_FROM_EMAIL = 'systems@mercycorps.org'
SERVER_EMAIL = app_settings.get('SERVER_EMAIL', None)
#DEFAULT_TO_EMAIL = 'to email'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8000',
    'http://localhost:8000',
)


