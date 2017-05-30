Tola Activity [![Build Status](https://travis-ci.org/toladata/TolaActivity.svg?branch=master)](https://travis-ci.org/toladata/TolaActivity)
====
http://toladata.com/products/activity/

TolaActivity extends the functionality of TolaData to include a set of forms and
reports for managing project activities for a WorkflowLevel1.  It includes workflow for approving
and completing projects as well as sharing the output data.

TolaActivity functionality http://www.github.com/toladata/TolaActivty is intended to allow importing
and exporting of project specific data from 3rd party data sources or excel
files.

## Configuration
Copy the tola/settings/local-sample.py to local.py and modify for your environment.

## To deploy changes in activity servers
Once all your changes have been commited to the repo, and before pushing them, run: 
`. travis.sh`

## To deploy locally via Docker
Run the following commands from the root of this repository:
  - `docker-compose build`
  - `docker-compose up`

## USING virtualenv
(Install virtualenv)
pip install virtualenv

# Create Virtualenv
virtualenv —no-site-packages venv
* use no site packages to prevent virtualenv from seeing your global packages

. venv/bin/activate
* allows us to just use pip from command line by adding to the path rather then full path

##Activate Virtualenv
source venv/bin/activate

## Fix probable mysql path issue (for mac)
export PATH=$PATH:/usr/local/mysql/bin
* or whatever path you have to your installed mysql_config file in the bin folder of mysql

pip install -r requirements.txt

## Set up DB
python manage.py migrate

# Run App
If your using more then one settings file change manage.py to point to local or dev file first
python manage.py runserver 0.0.0.0:8000
GOOGLE API
sudo pip install --upgrade google-api-python-client
* 0’s let it run on any local address i.e. localhost,127.0.0.1 etc.
