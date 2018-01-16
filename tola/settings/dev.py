from local import *


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = '/static'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'
########## END STATIC FILE CONFIGURATION

DEBUG = False

OFFLINE_MODE = True
INTERNAL_IPS = ('127.0.0.1',)

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/tola-messages'
