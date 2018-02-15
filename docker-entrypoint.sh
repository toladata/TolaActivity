#!/bin/bash
set -o xtrace

echo "Migrate"
python manage.py migrate

echo "Collect static files"
python manage.py collectstatic

RESULT=$?

nginx;

if [ $RESULT -eq 0 ]; then
    echo "Running the server"
    service nginx restart
    gunicorn -b 0.0.0.0:8080 tola.wsgi
else
    pushd templates2/maintenance/; python -m SimpleHTTPServer 8888; popd
fi
