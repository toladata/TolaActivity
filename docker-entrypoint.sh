#!/bin/bash
set -o xtrace

echo "Migrate"
python manage.py migrate

RESULT=$?

nginx;

if [ $RESULT -eq 0 ]; then
    echo "Running the server"
    gunicorn -b 127.0.0.1:8888 tola.wsgi
else
    pushd templates2/maintenance/; python -m SimpleHTTPServer 8888; popd
fi
