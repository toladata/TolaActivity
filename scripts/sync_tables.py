"""
import json data from API
IMPORTANT!! you must turn off pagination for this to work from a URL and get all
country records
Install module django-extensions
Runs twice via function calls at bottom once
"""

from tola.tables_sync import update_level1, update_level2


def run():
    print "Running Script..."
    try:
        update_level1()
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))

    try:
        update_level2()
    except Exception as e:
        print '%s (%s)' % (e.message, type(e))

