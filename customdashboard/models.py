from django.db import models
from django.contrib import admin
from django.conf import settings
from activitydb.models import Program
from datetime import datetime


class ProjectStatus(models.Model):
    project_status = models.CharField("Project Status", max_length=50, blank=True)
    description = models.CharField("Status Description", max_length=200, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.project_status


class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ('project_status','description','create_date','edit_date')
    display = 'Project Status'

