#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    if 'test' in sys.argv and '--tag=pkg' in sys.argv:
        settings = 'tola.settings.test_pkg'
        os.environ['DJANGO_SETTINGS_MODULE'] = settings
    elif 'test':
        settings = 'tola.settings.test'
        os.environ['DJANGO_SETTINGS_MODULE'] = settings
    elif os.environ.get("DJANGO_SETTINGS_MODULE"):
        settings = os.environ.get("DJANGO_SETTINGS_MODULE")
    else:
        settings = 'tola.settings.local'

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
