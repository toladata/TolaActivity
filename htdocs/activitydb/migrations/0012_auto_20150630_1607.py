# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0011_auto_20150630_0824'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('in_file', models.BooleanField()),
                ('not_applicable', models.BooleanField()),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('agreement', models.ForeignKey(blank=True, to='activitydb.ProjectAgreement', null=True)),
            ],
            options={
                'ordering': ('agreement',),
            },
        ),
        migrations.CreateModel(
            name='ChecklistItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.CharField(max_length=255, null=True, blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('country', models.ForeignKey(blank=True, to='activitydb.Country', null=True)),
            ],
            options={
                'ordering': ('item',),
            },
        ),
        migrations.AddField(
            model_name='checklist',
            name='item',
            field=models.ForeignKey(blank=True, to='activitydb.ChecklistItem', null=True),
        ),
    ]
