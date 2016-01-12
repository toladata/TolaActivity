# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0056_program_budget_check'),
        ('customdashboard', '0002_auto_20151109_1135'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link', models.CharField(max_length=200, verbose_name=b'Link to Service', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProgramLinks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(blank=True, max_length=255, null=True, verbose_name=b'Type of Link', choices=[(b'gallery', b'Gallery'), (b'map', b'MapBox Map Layer')])),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('link', models.ForeignKey(blank=True, to='customdashboard.Link', max_length=200)),
                ('program', models.ForeignKey(to='activitydb.Program', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProgramNarrative',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(max_length=200, verbose_name=b'Status Description', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('program', models.ForeignKey(to='activitydb.Program', blank=True)),
            ],
        ),
    ]
