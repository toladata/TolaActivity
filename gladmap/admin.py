from django.contrib import admin
from .models import Boundary, Country, State

# Register your models here.
admin.site.register(Boundary)
admin.site.register(Country)
admin.site.register(State)