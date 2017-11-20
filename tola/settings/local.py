from base import *
import os
from os.path import join, normpath

try:
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
except KeyError:
    # Fallback for tests without environment variables configured
    # Depends on os.environ for correct functionality
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'tolaactivity',
        }
    }
    print("DATABASES: {}".format(DATABASES))

# Hosts/domain names that are valid for this site
if os.getenv('TOLA_HOSTNAME') is not None:
    ALLOWED_HOSTS = os.getenv('TOLA_HOSTNAME').split(',')

USE_X_FORWARDED_HOST = True if os.getenv('TOLA_USE_X_FORWARDED_HOST') == 'True' else False

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
DEBUG = True if os.getenv('TOLA_DEBUG') == 'True' else False

CORS_ORIGIN_ALLOW_ALL = True

########## SOCIAL AUTH CLIENT CONFIG ###########
GOOGLE_STEP2_URI = ''
GOOGLE_CLIENT_ID = ''
GOOGLE_CLIENT_SECRET = ''
SOCIAL_AUTH_LOGIN_REDIRECT_URL = os.getenv('SOCIAL_AUTH_LOGIN_REDIRECT_URL')
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')

SOCIAL_AUTH_MICROSOFT_GRAPH_KEY = os.getenv('SOCIAL_AUTH_MICROSOFT_GRAPH_KEY')
SOCIAL_AUTH_MICROSOFT_GRAPH_SECRET = os.getenv('SOCIAL_AUTH_MICROSOFT_GRAPH_SECRET')
SOCIAL_AUTH_MICROSOFT_GRAPH_REDIRECT_URL = os.getenv('SOCIAL_AUTH_MICROSOFT_GRAPH_REDIRECT_URL')
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['redirect_after_login']


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
OFFLINE_MODE = False
NON_LDAP = True
LOCAL_API_TOKEN = "ABC"

# Configure templates for API only version
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [normpath(join(SITE_ROOT, 'templates2'))],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'builtins': [
                'django.contrib.staticfiles.templatetags.staticfiles',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.getenv('TOLA_ERROR_LOG', 'tola_activity_error.log'),
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

TOLA_TRACK_URL = os.getenv('TOLA_TRACK_URL')
TOLA_TRACK_TOKEN = os.getenv('TOLA_TRACK_TOKEN')

ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL')
ELASTICSEARCH_INDEX_PREFIX = os.getenv('ELASTICSEARCH_INDEX_PREFIX')
