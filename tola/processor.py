#add global variable for report server or not to all templates so we can hide elements that aren't wanted on the report server
from settings.local import REPORT_SERVER
from settings.local import OFFLINE_MODE

def report_server_check(request):
    return {'report_server': REPORT_SERVER, 'offline_mode': OFFLINE_MODE}
