from django.db import models
from django.contrib import admin
from activitydb.models import Program


LINK_TYPE_CHOICES = (
    ('gallery', 'Gallery'),
    ('map', 'MapBox Map Layer'),
)


class ProjectStatus(models.Model):
    project_status = models.CharField("Project Status", max_length=50, blank=True)
    description = models.CharField("Status Description", max_length=200, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.program__name


class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = ('project_status','description','create_date','edit_date')
    display = 'Project Status'


class Gallery(models.Model):
    program_name = models.ForeignKey(Program, null=True, blank=True)
    title = models.CharField("Title", max_length=100, unique=True)
    narrative = models.TextField("Narrative Text", max_length=200, blank=True)
    image_name = models.CharField("Image URL", max_length=50, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.program__name


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('project_status','title','create_date','edit_date')
    display = 'Gallery'


class OverlayGroups(models.Model):
    overlay_group = models.CharField("Overlay Group Name", max_length=50, unique=True)
    program = models.ForeignKey(Program, blank=True)
    json_url = models.CharField("geoJSON name", max_length=50, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.overlay_group


class OverlayGroupsAdmin(admin.ModelAdmin):
    list_display = ('overlay_group', 'json_url', 'create_date', 'edit_date')
    display = 'Overlay Group'


class OverlayNarratives(models.Model):
    overlay_title = models.CharField("Overlay Title", max_length=50, unique=True)
    program = models.ForeignKey(Program, blank=True)
    overlay_group = models.ForeignKey(OverlayGroups, blank=True)
    narrative_title = models.CharField("Narrative Title", max_length=100, blank=True)
    narrative = models.TextField("Narrative Text", blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.overlay_title


class OverlayNarrativesAdmin(admin.ModelAdmin):
    list_display = ('overlay_title', 'overlay_group', 'narrative', 'create_date', 'edit_date')
    display = 'Overlay Narrative'


class Link(models.Model):
    link = models.CharField("Link to Service", max_length=200, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.link


class LinkAdmin(admin.ModelAdmin):
    list_display = ('link','create_date','edit_date')
    display = 'Link'


class ProgramLinks(models.Model):
    program = models.ForeignKey(Program, blank=True)
    type = models.CharField("Type of Link",blank=True, null=True, max_length=255, choices=LINK_TYPE_CHOICES)
    link = models.ForeignKey(Link, max_length=200, blank=True)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):

        return self.title


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title','narrative','image_name','create_date','edit_date')
    display = 'Photo Gallery'


class ProgramLinksAdmin(admin.ModelAdmin):
    list_display = ('program','create_date','edit_date')
    display = 'Program Link'


class JupyterNotebooks(models.Model):
    name = models.CharField("Notebook Name", max_length=255)
    program = models.ForeignKey(Program, blank=True,null=True)
    very_custom_dashboard = models.CharField("Specialty Custom Dashboard Links",blank=True, null=True, max_length=255)
    file = models.FileField("HTML/Jupyter Nontebook File", blank=True,null=True,upload_to="media")
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Jupyter Notebooks"

    def __unicode__(self):

        return self.name



class JupyterNotebooksAdmin(admin.ModelAdmin):
    list_display = ('name','program','very_custom_dashboard','create_date','edit_date')
    display = 'Jupyter Notebooks'




