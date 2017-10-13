#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":

    if 'test' in sys.argv:
        settings = 'tola.settings.test'
    elif os.environ.get("DJANGO_SETTINGS_MODULE"):
        settings = os.environ.get("DJANGO_SETTINGS_MODULE")
    else:
        settings = 'tola.settings.local'

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
