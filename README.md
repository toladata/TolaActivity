# Tola Activity
[![Build Status](https://travis-ci.org/toladata/TolaActivity.svg?branch=master)](https://travis-ci.org/toladata/TolaActivity)

http://toladata.com/products/activity/

TolaActivity extends the functionality of TolaData to include a set
of forms and reports for managing project activities for a Program.
It includes workflow for approving and completing projects as well
as sharing the output data. TolaActivity functionality
http://www.github.com/toladata/TolaActivity is intended to allow
importing and exporting of project specific data from 3rd party
data sources or excel files.

# Setting up a local TolaActivity instance

Running a local instance of TolaActivity makes development much faster and
eliminates your dependence on access to MC's dev and demo and production
servers. These instructions should get you up and running with a minimum
of fuss.

## Install the bits

TolaActivity requires Python 2. We have chosen to use MySQL as Django's 
back-end.

### macOS

On macOS, you can use Homebrew to install Python 2 alongside the system
Python 2 installation as shown in the following:

```
$ brew install python@2
$ brew install pip
$ brew install mysql mysql-utilies
$ brew install py2cairo pango
$ git clone https://github.com/mercycorps.org/TolaActivity.git
$ git checkout dev
$ virtualenv TolaActivty --no-site-packages
$ cd TolaActivity
$ source bin/activate
$ mkdir config
$ # Place settings.secret.yml into config/ directory
$ pip install -r requirements.txt
$ pip install --upgrade google-api-python-client
$ cp tola/settings/local-sample.py tola/settings/local.py
```

Edit the configuration file as described in the next section.

### Ubuntu Linux, Linux Mate, and derivatives

On Ubuntu and its derivatives (this was done on Linux Mate 18), Python
2 is the default (true when written, this might change later), so the
following should get you going on any current Python 2 version for most
Ubuntu-family distros (could those be called, _Ubunten_?):

```
$ python --version
$ # Makse sure output from above indicates Python 2
$ sudo apt install mysql-server libmysqld-dev mysql-utilities mysql-client
$ git clone https://github.com/mercycorps.org/TolaActivity.git
$ git checkout dev
$ virtualenv TolaActivty --no-site-packages
$ cd TolaActivity
$ source bin/activate
$ mkdir config
$ # Place settings.secret.yml into config/ directory
$ pip install -r requirements.txt
$ pip install --upgrade google-api-python-client
$ cp tola/settings/local-sample.py tola/settings/local.py
$ vi tola/settings/local.py
```

Edit the configuration file as described in the next section.

## Modify the config file

Edit _tola/settings/local.py_. You will need to disable dependencies on
local apps and set the TolaActivity's MySQL and password. First, find the
section near the end of the file that looks like this:

```
########## LOCAL APPS DEPENDING ON SERVER DEBUG FOR DEV BOXES, REPORT BUILDER FOR REPORT SERVER
DEV_APPS = (
    'debug_toolbar',
)

INSTALLED_APPS = INSTALLED_APPS + DEV_APPS


DEV_MIDDLEWARE = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + DEV_MIDDLEWARE"
```

Comment out these sections as shown below:

```
# ########## LOCAL APPS DEPENDING ON SERVER DEBUG FOR DEV BOXES, REPORT BUILDER FOR REPORT SERVER
# DEV_APPS = (
#     'debug_toolbar',
# )
#
# INSTALLED_APPS = INSTALLED_APPS + DEV_APPS
#
#
# DEV\_MIDDLEWARE = (
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# )
#
# MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + DEV_MIDDLEWARE
```

In the database configuration section, set the appropriate value for
`PASSWORD`. Don't change the `USER` entry unless you know why you need
to.

```
        'USER': 'admin',
        'PASSWORD': 'SekritWord',
```

Save your changes and exit the file.

## Set up Django

Next, Set up the Django database:

```
$ python manage.py migrate

Operations to perform:
  Apply all migrations: admin, auth, authtoken, contenttypes, customdashboard, formlibrary, indicators, reports, sessions, sites, social_django, workflow
  Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK

  [output deleted]

  Applying workflow.0014_remove_stakeholder_sector... OK
  Applying workflow.0015_stakeholder_notes... OK
  Applying workflow.0016_auto_20170623_1306... OK
```

Start the server:

```
$ python manage.py runserver
Performing system checks...

System check identified 1 issue (0 silenced).
March 20, 2018 - 11:51:55
Django version 1.11.2, using settings 'tola.settings.local'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.


```

## Configuring OAuth authentication

When running a local instance, we use Google's OAuth API to control 
access and authentication to TolaActivity. There exists a bug in the
API library that requires an ugly manual workaround before you can
actually log in and starting using TolaActivity.

* Start the TA server
* Browse to the home page
* Click the "Google+" link below the login button to authenticate with
Google Auth.
* Select your username and login
* You'll get this error screen. That means you've hit the bug.
* Stop the TA server
* Log in to your MySQL instance
* Get the user ID google added
* Insert that into the the Workflow_tolauser table
* Restart the TA server
* Refresh the browser window
* Rejoice!

