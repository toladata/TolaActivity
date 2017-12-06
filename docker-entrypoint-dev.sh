#!/bin/bash

echo "Collect static files"
python manage.py collectstatic -v 0 --noinput

echo "Migrate"
python manage.py migrate

echo "Creating admin user"
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(email='admin@humanitec.com').delete(); User.objects.create_superuser('admin', 'admin@humanitec.com', 'admin')"

echo "Loading basic initial data"
python manage.py loadinitialdata

echo "Running the server"
PYTHONUNBUFFERED=1 python manage.py runserver 0.0.0.0:8080
