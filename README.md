Tola Activity [![Build Status](https://travis-ci.org/toladata/TolaActivity.svg?branch=master)](https://travis-ci.org/toladata/TolaActivity)

http://toladata.com/products/activity/

TolaActivity extends the functionality of TolaData to include a set
of forms and reports for managing project activities for a Program.
It includes workflow for approving and completing projects as well
as sharing the output data. TolaActivity functionality
http://www.github.com/toladata/TolaActivity is intended to allow
importing and exporting of project specific data from 3rd party
data sources or excel
files.


# Setting up a local TolaActivity instance

Running a local instance of TolaActivity makes development much faster and
eliminates your dependence on access to MC's dev and demo and production
servers. These instructions should get you up and running with a minimum of
fuss.

## Install the bits

You will need Python 2 and MySQL installed because TolaActivity requires v2
of Python.

### macOS

On macOS, you can use Homebrew to install Python 2 alongside the system
Python 2 installation as shown in the following:

```
$ brew install python@2
$ brew install pip
$ brew install mysql mysql-utilies
$ git clone https://github.com/mercycorps.org/TolaActivity.git
$ virtualenv TolaActivty --no-site-packages
$ cd TolaActivity
$ mkdir config
$ source bin/activate
$ pip install -r requirements.txt
$ cp tola/settings/local-sample.py tola/settings/local.py
$ vi tola/settings/local.py
```

### Ubuntu Linux, Linux Mate, and derivatives

On Ubuntu and its derivatives (this was done on Linux Mate 18), Python 2 is the
default (true when written, this might change later), so the following should
get you going on any current Python 2 version:

```
$ python --version
$ # Makse sure output from above indicates Python 2
$ sudo apt install mysql-server libmysqld-dev mysql-utilities mysql-client
$ git clone https://github.com/mercycorps.org/TolaActivity.git
$ virtualenv TolaActivty --no-site-packages
$ cd TolaActivity
$ source bin/activate
$ mkdir config
$ # Place settings.secret.yml into config/ directory
$ pip install -r requirements.txt
$ cp tola/settings/local-sample.py tola/settings/local.py
$ vi tola/settings/local.py
```

Edit _tola/settings/local.py_. You will need to disable dependencies
on local apps and set a MySQL username and password. First, find the
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

In the database configuration section, change the `USER:` value to `root` and:

```
        'USER': 'root',
        'PASSWORD': 'NewPassword',
```

Save your changes and exit the file.

## Set up Django

Next, Set up the Django database:

```
$ python manage.py migrate
System check identified some issues:

WARNINGS:
?: (1\_8.W001) The standalone TEMPLATE_* settings were deprecated in Django 1.8 and the TEMPLATES dictionary takes precedence. You must put the values of the following settings into your default TEMPLATES dict: TEMPLATE_DEBUG.
Operations to perform:
  Apply all migrations: admin, auth, authtoken, contenttypes, customdashboard, formlibrary, indicators, reports, sessions, sites, social_django, workflow
  Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK

  [additional output elided]

  Applying workflow.0014_remove_stakeholder_sector... OK
  Applying workflow.0015_stakeholder_notes... OK
  Applying workflow.0016_auto_20170623_1306... OK
```

Start the server:

```
$ python manage.py runserver 0.0.0.0:8000
Performing system checks...

System check identified some issues:

WARNINGS:
?: (1_8.W001) The standalone TEMPLATE_* settings were deprecated in Django 1.8 and the TEMPLATES dictionary takes precedence. You must put the values of the following settings into your default TEMPLATES dict: TEMPLATE_DEBUG.

System check identified 1 issue (0 silenced).
March 20, 2018 - 11:51:55
Django version 1.11.2, using settings 'tola.settings.local'
Starting development server at http://0.0.0.0:8000/
Quit the server with CONTROL-C.


```

Rejoice!

## Ignore This 

### To deploy changes in activity servers
Once all your changes have been commited to the repo, and before pushing them, run:
`. travis.sh`

### To deploy locally via Docker
Run the following commands from the root of this repository:
  - `docker-compose build`
  - `docker-compose up`

### GOOGLE API
sudo pip install --upgrade google-api-python-client
* 0’s let it run on any local address i.e. localhost,127.0.0.1 etc.
