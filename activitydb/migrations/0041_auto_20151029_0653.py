# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0040_auto_20151029_0643'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteprofile',
            name='populations_owning_livestock',
        ),
        migrations.AddField(
            model_name='siteprofile',
            name='households_owning_livestock',
            field=models.IntegerField(help_text='(%)', null=True, verbose_name='Households Owning Livestock', blank=True),
        ),
    ]
