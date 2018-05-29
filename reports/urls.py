from .views import *
from django.conf.urls import *


# place app url patterns here

urlpatterns = [                       # display reports
                       url(r'^report/$', ReportHome.as_view(), name='report_home'),

                       ]
