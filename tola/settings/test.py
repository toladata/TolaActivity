from local import *

ADMINS = (
    ('admin_test', 'admin_test@test.com'),
)

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/tola-messages'

ELASTICSEARCH_ENABLED = False
