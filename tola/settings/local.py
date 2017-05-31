from base import *


########## IN-MEMORY TEST DATABASE
import os

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
from os.path import join, normpath

########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('test', 'test@test.com'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
########## END EMAIL CONFIGURATION

########## EMAIL SETTINGS

########## END EMAIL SETTINGS

CORS_ORIGIN_ALLOW_ALL = True

########## GOOGLE CLIENT CONFIG ###########
GOOGLE_STEP2_URI = ''
GOOGLE_CLIENT_ID = ''
GOOGLE_CLIENT_SECRET = ''


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION

######## If report server then limit navigation and allow access to public dashboards
REPORT_SERVER = False
OFFLINE_MODE = True
NON_LDAP = True
LOCAL_API_TOKEN = "ABC"



