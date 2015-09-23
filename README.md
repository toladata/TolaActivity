Tola Activity
====
http://mercycorps.github.io/tola-activity

Tola activity extends the functionality of Tola data to include a set of forms and
reports for managing project activities for a Program.  It includes workflow for approving
and completing projects as well as sharing the output data.

Tola Data fucntionality http:www.github.com/mercycorps/tola is intended to allow importing
and exporting of project specific data from 3rd party data sources or excel
files.  

## USING virtualenv
mkdir frds_project
cd frds_project
(Install virtualenv)
pip install virtualenv

cd frds_project

# Create Virtualenv
virtualenv —no-site-packages frds-venv
* use no site packages to prevent virtualenv from seeing your global packages

. frds-venv/bin/activate
* allows us to just use pip from command line by adding to the path rather then full path

##Activate Virtualenv
source frds-venv/bin/activate

## Fix probable mysql path issue (for mac)
export PATH=$PATH:/usr/local/mysql/bin
* or whatever path you have to your installed mysql_config file in the bin folder of mysql

pip install -r requirements.txt

## Set up DB
python manage.py syncdb

# Run App
If your using more then one settings file change manage.py to point to local or dev file first
python manage.py runserver 0.0.0.0:8000
GOOGLE API
sudo pip install --upgrade google-api-python-client
* 0’s let it run on any local address i.e. localhost,127.0.0.1 etc.
