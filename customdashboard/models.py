from django.db import models
from django.contrib import admin

from workflow.models import WorkflowLevel1


class JupyterNotebooks(models.Model):
    name = models.CharField("Notebook Name", max_length=255)
    workflowlevel1 = models.ForeignKey(WorkflowLevel1, blank=True, null=True)
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
    list_display = ('name','workflowlevel1','very_custom_dashboard','create_date','edit_date')
    display = 'Jupyter Notebooks'

