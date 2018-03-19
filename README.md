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


=Setting up a local TolaActivity instance

Running a local instance of TolaActivity makes development much faster and
eliminates your dependence on access to MC's dev and demo and production
servers. These instructions should get you up and running with a minimum of
fuss.

==Install the bits

You will need Python 2 and MySQL installed because TolaActivity requires v2
of Python.  On macOS, you can use Homebrew to install Python 2 alongside
the system Python 2 installation as show in the following:

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

Edit _tola/settings/local.py_. Find the section at the end of the file that looks like this:

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

Comment out these sections as show in the following:

```
# ########## LOCAL APPS DEPENDING ON SERVER DEBUG FOR DEV BOXES, REPORT BUILDER FOR REPORT SERVER
# DEV_APPS = (
#     'debug_toolbar',
# )
#
# INSTALLED_APPS = INSTALLED_APPS + DEV_APPS
#
#
# DEV_MIDDLEWARE = (
#     'debug_toolbar.middleware.DebugToolbarMiddleware',
# )
#
# MIDDLEWARE_CLASSES = MIDDLEWARE_CLASSES + DEV_MIDDLEWARE
#
######## If report server then limit navigation and allow access to public dashboards
```

Set up the Django databse:

```
$ python manage.py migrate
```

Start the server:

```
$ python manage.py runserver 0.0.0.0:8000
```

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
