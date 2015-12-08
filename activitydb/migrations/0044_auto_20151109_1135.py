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
                ('dashboard_name', models.CharField(max_length=255, verbose_name='Custom Dashboard Name', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('dashboard_name',),
            },
        ),
        migrations.AddField(
            model_name='program',
            name='dashboard_name',
            field=models.ForeignKey(blank=True, to='activitydb.CustomDashboard', null=True),
        ),
    ]
