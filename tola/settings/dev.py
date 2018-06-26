from local import *

DEBUG = True

OFFLINE_MODE = True
INTERNAL_IPS = ('127.0.0.1',)

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/tola-messages'
