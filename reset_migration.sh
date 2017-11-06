#!/bin/bash

echo "#### Clear the migration history ####"
python manage.py migrate --fake customdashboard zero
python manage.py migrate --fake formlibrary zero
python manage.py migrate --fake indicators zero
python manage.py migrate --fake reports zero
python manage.py migrate --fake workflow zero

echo "#### Delete old migration scripts ####"
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

echo "#### Create the initial migrations ####"
python manage.py makemigrations

echo "#### Fake the initial migration ####"
python manage.py migrate --fake-initial