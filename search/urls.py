from django.conf.urls import include, url
from .views import search_index
from indicators import views as indicatorviews

urlpatterns = [
    url(r'^update_index', search_index, name='search_index'),

]