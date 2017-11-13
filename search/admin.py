# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import SearchIndexLog, SearchIndexLogAdmin

from django.contrib import admin

# Register your models here.
SearchIndexLog

admin.site.register(SearchIndexLog, SearchIndexLogAdmin)