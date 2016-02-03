#add global variable for report server or not to all templates so we can hide elements that aren't wanted on the report server
from settings.local import REPORT_SERVER
from settings.local import ACTIVITY_UP

def report_server_check(request):
    return {'report_server': REPORT_SERVER}

def server_status(request):
    return {'server_up': ACTIVITY_UP}