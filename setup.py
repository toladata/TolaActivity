# -*- coding: utf-8 -*-
import os
from os.path import join, dirname, abspath
from pkgutil import extend_path
from setuptools import find_packages, setup
import shutil

with open(join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# Allow setup.py to be run from any path
os.chdir(os.path.normpath(join(abspath(__file__), os.pardir)))


def load_requirements():
    return open(join(dirname(__file__), 'requirements-pkg.txt')).readlines()

shutil.copy('__init__.py', '__init__.py.bak')
shutil.copy('__init__.lib.py', '__init__.py')

setup(
    name='tola_activity',
    version='2.0',
    install_requires=load_requirements(),
    packages=[
        'factories',
        'formlibrary.migrations',
        'indicators.migrations',
        'workflow.migrations',
    ],
    py_modules=[
        '__init__',
        # formlibrary
        'formlibrary.admin',
        'formlibrary.models',
        # indicators
        'indicators.admin',
        'indicators.models',
        # search
        'search.admin',
        'search.apps',
        'search.exceptions',
        'search.models',
        'search.utils',
        # search.management.commands
        'search.management.__init__',
        'search.management.commands.__init__',
        'search.management.commands.search-index',
        # tola
        'tola.__init__',
        # tola.management.commands
        'tola.management.__init__',
        'tola.management.commands.__init__',
        'tola.management.commands.loadinitialdata',
        # workflow
        'workflow.admin',
        'workflow.apps',
        'workflow.models',
        'workflow.signals',
    ],
    description=('Workflow, visualizations and data services for managing NGO '
                 'projects and programs.'),
    url='https://github.com/toladata/TolaActivity',
    long_description=README,
    author=u'Rafael Muñoz Cárdenas',
    author_email='rafael@humanitec.com',
)

shutil.move('__init__.py.bak', '__init__.py')
