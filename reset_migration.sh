#!/bin/bash

echo "#### Clear the migration history ####"
python manage.py migrate --fake customdashboard zero
python manage.py migrate --fake formlibrary zero
python manage.py migrate --fake indicators zero
python manage.py migrate --fake reports zero
python manage.py migrate --fake workflow zero

echo "#### Fake the initial migration ####"
python manage.py migrate --fake-initial