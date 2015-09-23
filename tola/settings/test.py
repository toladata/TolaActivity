from base import *


########## IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}
"""Development settings and globals."""

from os.path import join, normpath


#from mongoengine import connect

########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('glind', 'glind@mercycorps.org'),
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
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
########## END EMAIL CONFIGURATION

########## EMAIL SETTINGS

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'systems@mercycorps.org'
EMAIL_HOST_PASSWORD = 'MCSys2015'
DEFAULT_FROM_EMAIL = 'systems@mercycorps.org'
SERVER_EMAIL = "glind@mercycorps.org"
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#DEFAULT_TO_EMAIL = 'to email'

########## END EMAIL SETTINGS


########## MongoDB Connect

#connect('feeds')

########## END DATABASE CONFIGURATION

########## GOOGLE CLIENT CONFIG ###########
GOOGLE_STEP2_URI = 'http://tola.mercycorps.org/gwelcome'
GOOGLE_CLIENT_ID = '617113120802.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '9reM29qpGFPyI8TBuB54Z4fk'


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
########## END CACHE CONFIGURATION

########## LOCAL DEV APPS
DEV_APPS = (
    'debug_toolbar',
)

INSTALLED_APPS = INSTALLED_APPS + DEV_APPS




