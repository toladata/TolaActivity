#!/bin/bash

echo "Migrate"
python manage.py migrate

RESULT=$?
if [ $RESULT -eq 0 ]; then
    echo "Running the server"
    gunicorn -b 0.0.0.0:8000 tola.wsgi
else
    pushd templates2/maintenance/; python -m SimpleHTTPServer 8000; popd
fi
