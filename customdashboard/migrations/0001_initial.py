# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0043_auto_20151102_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomDashboard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dashboard_name', models.CharField(max_length=200, blank=True)),
                ('program', models.ForeignKey(blank=True, to='activitydb.Program', null=True)),
                ('project_agreement', models.ForeignKey(blank=True, to='activitydb.ProjectAgreement', null=True)),
                ('project_completion', models.ForeignKey(blank=True, to='activitydb.ProjectComplete', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProjectStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_status', models.CharField(max_length=50, blank=True)),
                ('description', models.CharField(max_length=200, blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
        ),
    ]
