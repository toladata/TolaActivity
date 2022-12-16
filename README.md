# Tola Activity [![Build Status](https://travis-ci.org/toladata/TolaActivity.svg?branch=master)](https://travis-ci.org/toladata/TolaActivity) [![Coverage Status](https://coveralls.io/repos/github/toladata/TolaActivity/badge.svg)](https://coveralls.io/github/toladata/TolaActivity)


TolaActivity extends the functionality of TolaData to include a set of forms and
reports for managing project activities for a WorkflowLevel1.  It includes workflow for approving
and completing projects as well as sharing the output data.

TolaActivity functionality http://www.github.com/toladata/TolaActivity is intended to allow importing
and exporting of project specific data from 3rd party data sources or excel
files.


## Configuration

Location of settings:

* Development: `tola/settings/dev.py`
* Test runner: `tola/settings/test.py` and `tola/settings/test_pkg.py`
* Staging/Production: `tola/settings/local.py`

Check the documentation on setting up search functionality in `search/Readme.md`


## Deploy locally via Docker

Build first the images:

```bash
docker-compose -f docker-compose-dev.yml build
```

To run the webserver (go to 127.0.0.1:8080):

```bash
docker-compose -f docker-compose-dev.yml up # -d for detached
```

User: `admin`
Password: `admin`.

To run the tests:

```bash
docker-compose -f docker-compose-dev.yml run --entrypoint '/usr/bin/env' --rm web python manage.py test # --keepdb to run second time faster
```

To run the package building tests, follow these steps:

```bash
docker-compose -f docker-compose-dev.yml run --entrypoint '/usr/bin/env' --rm web bash
# Now inside the container
pip freeze | grep -v "^-e" | xargs pip uninstall -y; pip uninstall -y social_auth_core; cat requirements/base.txt | grep "^Django==\|^psycopg2" | xargs pip install; pip install -r requirements/pkg.txt
python manage.py test --tag=pkg --keepdb
```

To run the webserver with pdb support:

```bash
docker-compose -f docker-compose-dev.yml run --rm --service-ports web
```

To run bash:

```bash
docker-compose -f docker-compose-dev.yml run --entrypoint '/usr/bin/env' --rm web bash
```

or if you initialized already a container:

```bash
docker exec -it web bash
```

To connect to the database when the container is running:

```bash
docker exec -it postgres psql -U root tola_activity
```

If the database is empty, you may want to populate extra demo data to play
around with Activity:

```bash
docker-compose -f docker-compose-dev.yml run --entrypoint '/usr/bin/env' --rm web python manage.py loadinitialdata  --demo
```

(Be careful using this, only on demo!) If the database is already populated and
you want to restore the default data:

```bash
docker-compose -f docker-compose-dev.yml run --entrypoint '/usr/bin/env' --rm web python manage.py loadinitialdata  --restore
```

#### Issue with the local environment

If you're getting an error in your local environment, it can be related to 
the `social-core` library. To solve this issue you need to execute the 
following step:

- With the container running, go into it with this command:
  
  `docker exec -it web bash`
  
- Install the `social-core` lib again:

  `pip install -e git://github.com/toladata/social-core#egg=social-core`

- Now, restart the container.

It should solve the problem!


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
pip install -r requirements/dev.txt
```

Set up database:

```bash
python manage.py migrate
```

Run the server:

```bash
python manage.py runserver 0.0.0.0:8000
```

## Creating PRs and Issues
The following templates were created to easy the way to create tickets and help the developer.

- Bugs and Issues [[+]](https://github.com/toladata/TolaActivity/issues/new)
- New features [[+]](https://github.com/toladata/TolaActivity/issues/new?template=new_features.md)
- Pull requests [[+]](https://github.com/toladata/TolaActivity/compare/dev-v2?expand=1)
