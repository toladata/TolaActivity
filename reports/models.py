from django.db import models
from django.contrib import admin
from workflow.models import WorkflowLevel1, WorkflowLevel2, Country
from indicators.models import Indicator, CollectedData


class Report(models.Model):
    country = models.ForeignKey(Country)
    workflowlevel1 = models.ForeignKey(WorkflowLevel1, null=True, blank=True)
    workflowlevel2 = models.ForeignKey(WorkflowLevel2, null=True, blank=True)
    indicator = models.ForeignKey(Indicator, null=True, blank=True)
    collected = models.ForeignKey(CollectedData, null=True, blank=True)
    description = models.CharField("Status Description", max_length=200, blank=True)
    shared = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    create_date = models.DateTimeField(null=True, blank=True)
    edit_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('auth.User', related_name='reports', null=True, blank=True, on_delete=models.SET_NULL)

    def __unicode__(self):
        return self.workflowlevel1.name


class ReportAdmin(admin.ModelAdmin):
    list_display = ('country','workflowlevel1','description','create_date','edit_date')
    display = 'Project Status'





