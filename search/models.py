# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import uuid


class SearchIndexLog(models.Model):
    create_date = models.DateTimeField(null=True, blank=True)
    document_count = models.IntegerField(default=0)

    # on save add create date or update edit date
    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = datetime.now()
        super(SearchIndexLog, self).save()

    # displayed in admin templates
    def __unicode__(self):
        return unicode("Search Index log "+str(self.id))
