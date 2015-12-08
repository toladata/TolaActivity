# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0041_auto_20151029_0653'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormEnabled',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('agreement', models.ForeignKey(blank=True, to='activitydb.ProjectAgreement', null=True)),
                ('country', models.ForeignKey(blank=True, to='activitydb.Country', null=True)),
            ],
            options={
                'ordering': ('country', 'agreement'),
            },
        ),
        migrations.CreateModel(
            name='FormLibrary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Form Name', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('name', 'create_date'),
            },
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='district',
            field=models.ForeignKey(verbose_name='Administrative Level 2', blank=True, to='activitydb.District', null=True),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='province',
            field=models.ForeignKey(verbose_name='Administrative Level 1', blank=True, to='activitydb.Province', null=True),
        ),
        migrations.AlterField(
            model_name='siteprofile',
            name='village',
            field=models.CharField(max_length=255, null=True, verbose_name='Administrative Level 3', blank=True),
        ),
        migrations.AddField(
            model_name='formenabled',
            name='form',
            field=models.ForeignKey(to='activitydb.FormLibrary'),
        ),
    ]
