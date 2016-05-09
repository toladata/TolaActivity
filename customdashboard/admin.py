from django.contrib import admin

from .models import ProjectStatus, ProjectStatusAdmin, Gallery, GalleryAdmin, ProgramLinks,ProgramLinksAdmin, Link, LinkAdmin


class GalleryAdmin(admin.ModelAdmin):
    change_form_template = 'customdashboard/admin/change_form.html'

admin.site.register(ProjectStatus, ProjectStatusAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(ProgramLinks, ProgramLinksAdmin)
admin.site.register(Link, LinkAdmin)







