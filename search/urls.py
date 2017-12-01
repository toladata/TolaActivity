from django.conf.urls import include, url
from .views import *
from indicators import views as indicatorviews



urlpatterns = [
    #url(r'^update_index', search_index, name='search_index'),
    url(r'^get/(?P<index>\w+)/(?P<term>\w+)', search),

]