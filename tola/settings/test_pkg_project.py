INSTALLED_APPS += [
    'django.contrib.sites',

    # tola-activity dependencies
    #'oauth2_provider',

    # tola-activity apps
    'formlibrary',
    'workflow',
    'indicators',
    'search',
    'tola',
]

DATABASES = {
    'default': {
        'ENGINE': os.environ["TOLA_DB_ENGINE"],
        'NAME': os.environ["TOLA_DB_NAME"],
        'USER': os.environ["TOLA_DB_USER"],
        'PASSWORD': os.environ.get("TOLA_DB_PASS"),
        'HOST': os.environ.get("TOLA_DB_HOST", "localhost"),
        'PORT': os.environ.get("TOLA_DB_PORT", 5432),
    }
}
