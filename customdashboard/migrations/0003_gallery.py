# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0055_auto_20151216_1555'),
        ('customdashboard', '0002_auto_20151109_1135'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=100, verbose_name=b'Title')),
                ('narrative', models.TextField(verbose_name=b'Narrative Text', blank=True)),
                ('image_name', models.CharField(max_length=50, verbose_name=b'Image URL', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('program_name', models.ForeignKey(blank=True, to='activitydb.Program', null=True)),
            ],
        ),
    ]
