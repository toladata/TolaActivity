from .views import *
from django.conf.urls import *


# place app url patterns here

urlpatterns = patterns('',

                       #display reports
                       url(r'^report/$', ReportHome.as_view(), name='report_home'),
                       url(r'^report_data/', ReportData.as_view(), name='report_data'),
                       )
