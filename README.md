# Tola Activity [![Build Status](https://travis-ci.org/toladata/TolaActivity.svg?branch=master)](https://travis-ci.org/toladata/TolaActivity)

http://toladata.com/products/activity/

TolaActivity extends the functionality of TolaData to include a set of forms and
reports for managing project activities for a WorkflowLevel1.  It includes workflow for approving
and completing projects as well as sharing the output data.

TolaActivity functionality http://www.github.com/toladata/TolaActivity is intended to allow importing
and exporting of project specific data from 3rd party data sources or excel
files.


## Configuration

Location of settings:

* Development: `tola/settings/dev.py`
* Test runner: `tola/settings/test.py`
* Staging/Production: `tola/settings/local.py`


## Deploy changes in activity servers

Once all your changes have been commited to the repo, and before pushing them, run:
`. travis.sh`


## Deploy locally via Docker

Build first the images:

```bash
docker-compose -f docker-compose-dev.yml build
```

To run the webserver:

```bash
docker-compose -f docker-compose-dev.yml up # -d for detached
```

User: `admin`
Password: `admin`.

To run the tests:

```bash
docker-compose -f docker-compose-dev.yml run --entrypoint '/usr/bin/env' --rm web python manage.py test # --keepdb to run second time faster
```

To run bash:

```bash
docker -f docker-compose-dev.yml run --entrypoint '/usr/bin/env' --rm web bash
```

or if you initialized already a container:

```bash
docker exec -it web bash
```

To connect to the database when the container is running:

```bash
docker exec -it postgres psql -U root tola_activity
```

## Deploy locally using virtualenv

Given pip is installed:

```bash
pip install virtualenv
```

Create the environment:

```bash
virtualenv —no-site-packages venv
````

Note: use no site packages to prevent virtualenv from seeing your global packages.

Activate the environment:

```bash
. venv/bin/activate
```

or:

```bash
source venv/bin/activate
```

Install requirements:

```bash
pip install -r requirements-dev.txt
```

Set up database:

```bash
python manage.py migrate
```

Run the server:

```bash
python manage.py runserver 0.0.0.0:8000
```

