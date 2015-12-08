from django.contrib import admin

from .models import ProjectStatus, ProjectStatusAdmin

admin.site.register(ProjectStatus, ProjectStatusAdmin)






