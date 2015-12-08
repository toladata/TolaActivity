# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0026_auto_20151026_0133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siteprofile',
            name='altitude',
        ),
        migrations.RemoveField(
            model_name='siteprofile',
            name='approval',
        ),
        migrations.RemoveField(
            model_name='siteprofile',
            name='distance_district_capital',
        ),
        migrations.RemoveField(
            model_name='siteprofile',
            name='distance_field_office',
        ),
        migrations.RemoveField(
            model_name='siteprofile',
            name='distance_site_camp',
        ),
        migrations.RemoveField(
            model_name='siteprofile',
            name='existing_village',
        ),
        migrations.RemoveField(
            model_name='siteprofile',
            name='existing_village_descr',
        ),
        migrations.RemoveField(
            model_name='siteprofile',
            name='precision',
        ),
        migrations.AddField(
            model_name='siteprofile',
            name='info_source',
            field=models.CharField(max_length=255, null=True, verbose_name='Data Source', blank=True),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='name',
            field=models.CharField(default=datetime.datetime(2015, 10, 27, 21, 6, 36, 467369, tzinfo=utc), max_length=255, verbose_name='Site Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='village',
            field=models.CharField(help_text='Village', max_length=255, null=True, verbose_name='Administrative Level 3', blank=True),
        ),
    ]
