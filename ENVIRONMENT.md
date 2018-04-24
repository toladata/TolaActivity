# Environment configuration

The following environment variables have to be set in order for the application to run correctly.

### General
* `DEFAULT_ORG` Name for the default organization
* `DEFAULT_OAUTH_DOMAINS` Default Domain used for OAuth Authentication
* `TOLA_ACTIVITY_URL` URL for redirecting to TolaActivity
* `TOLA_TRACK_URL` URL for redirecting to TolaTrack
* `TOLA_TRACK_TOKEN` Token to access the TolaTrack API

### Database
* `TOLA_DB_ENGINE` Configuration for Django Database engine. Valid options are defined 
in the [Django Documentation](https://docs.djangoproject.com/en/2.0/ref/settings/#engine)
* `TOLA_DB_NAME` Database name
* `TOLA_DB_USER` Username for the database
* `TOLA_DB_PASS` Password for the database
* `TOLA_DB_HOST` Database Hostname or IP-Address
* `TOLA_DB_PORT` Database Port (default for postgresql is `5432`, for mysql `3306`)
* `TOLA_DEBUG` `True` or `False` value specifying if 
[Django Debug mode](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-DEBUG) should be enabled
* `TOLA_TEMPLATE_DIR` Specifies the template directory for Django templates 
(should be set to `templates` for Django default)
* `TOLA_ERROR_LOG` Path to the logfile for errors
* `TOLA_HOSTNAME` Sets the `ALLOWED_HOSTS` settings in Django.
 See [Django Doc](https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts)
* `TOLA_USE_X_FORWARDED_HOST` `True` or `False` value specifying if `USE_X_FORWARDED_HOST` should be enabled
See [Django Doc](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-USE_X_FORWARDED_HOST)
* `TOLA_USE_HTTPS` `True` or `False` value specifying if `SECURE_PROXY_SSL_HEADER` should be set to `https`
See [Django Doc](https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-SECURE_PROXY_SSL_HEADER)

### Social Auth Login/Signup
* `SOCIAL_AUTH_REDIRECT_IS_HTTPS` Value should be `True` or `False`, specifies if social auth will redirect to HTTPS
* `SOCIAL_AUTH_GOOGLE_OAUTH2_KEY` Only needed for Social Auth with Google, OAUTH2 Application Key obtained 
from [Google](https://developers.google.com/identity/protocols/OAuth2)
* `SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET` The secret associated with the key defined above
* `SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS` If using Google OAuth with company accounts, users with EMail addresses
 using the domains defined here can automatically sign up and create an account.
* `SOCIAL_AUTH_MICROSOFT_WHITELISTED_DOMAINS` If using Microsoft OAuth with company accounts, users with EMail addresses
 using the domains defined here can automatically sign up and create an account.
* `SOCIAL_AUTH_MICROSOFT_GRAPH_REDIRECT_URL` The redirect URL for this application. 
Should point to `/complete/microsoft-graph` on the server the application is running on
* `SOCIAL_AUTH_MICROSOFT_GRAPH_KEY` Key for using Microsoft OAUTH2 APIs. 
Generated in the [Microsoft Application Registration Portal](https://apps.dev.microsoft.com/)
* `SOCIAL_AUTH_MICROSOFT_GRAPH_SECRET` The secret obtained with the Key
* `SOCIAL_AUTH_LOGIN_REDIRECT_URL` The default URL the user should be redirected to after successful Social-Auth login

### Chargebee
Configuration necessary to work with Chargebee integration
* `CHARGEBEE_SITE_API_KEY` API Key obtained by Chargebee
* `CHARGEBEE_SITE` Sitename for Chargebee

### Search

The following environment variables are required to run with search enabled.

* `ELASTICSEARCH_ENABLED` decides whether objects saved to the database will also be indexed in elasticsearch. The search will work without it but only with existing data. This can be used if a lot of data is imported that should not be immediately indexed in ES.
* `ELASTICSEARCH_URL` sets the URL for connecting with the ES cluster.
* `ELASTICSEARCH_INDEX_PREFIX` sets a prefix for each index. There will be many indices for our instances and its important that we don't mix them up. Each index in the background will be created and named automatically, but we can set the prefix to separate between the servers.

