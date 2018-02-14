from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^get/(?P<index>\w+)/(?P<term>\w+)', search),
]