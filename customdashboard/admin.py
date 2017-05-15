from .models import *


class GalleryAdmin(admin.ModelAdmin):
    change_form_template = 'customdashboard/admin/change_form.html'

admin.site.register(JupyterNotebooks, JupyterNotebooksAdmin)







