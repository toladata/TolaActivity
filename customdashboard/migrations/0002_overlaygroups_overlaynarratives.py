# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customdashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OverlayGroups',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('overlay_group', models.CharField(unique=True, max_length=50, verbose_name=b'Overlay Group Name')),
                ('json_url', models.CharField(max_length=50, verbose_name=b'geoJSON name', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OverlayNarratives',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('overlay_title', models.CharField(unique=True, max_length=50, verbose_name=b'Overlay Title')),
                ('narrative_title', models.CharField(max_length=100, verbose_name=b'Narrative Title', blank=True)),
                ('narrative', models.TextField(verbose_name=b'Narrative Text', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('overlay_group', models.ForeignKey(to='customdashboard.OverlayGroups', blank=True)),
                ('program', models.ForeignKey(to='activitydb.Program', blank=True)),
            ],
        ),
    ]
