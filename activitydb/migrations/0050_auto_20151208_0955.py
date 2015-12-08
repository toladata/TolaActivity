# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activitydb', '0049_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='LandType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('classify_land', models.CharField(help_text='Rural, Urban, Peri-Urban', max_length=100, verbose_name='Land Classification', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('classify_land',),
            },
        ),
        migrations.DeleteModel(
            name='TolaUser',
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='approval',
            field=models.CharField(default='in progress', max_length=255, null=True, verbose_name='Approval Status', blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='actual_budget',
            field=models.CharField(help_text='What was the actual final cost?  This should match any financial documentation you have in the file.   It should be completely documented and verifiable by finance and any potential audit', max_length=255, null=True, verbose_name='Actual Cost', blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='approval',
            field=models.CharField(default='in progress', max_length=255, null=True, verbose_name='Approval Status', blank=True),
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='budget_variance',
            field=models.CharField(max_length=255, null=True, verbose_name='Budget versus Actual variance', blank=True),
        ),
        migrations.CreateModel(
            name='TolaUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(blank=True, max_length=3, null=True, choices=[('mr', 'Mr.'), ('mrs', 'Mrs.'), ('ms', 'Ms.')])),
                ('name', models.CharField(max_length=100, null=True, verbose_name='Given Name', blank=True)),
                ('employee_number', models.IntegerField(null=True, verbose_name='Employee Number', blank=True)),
                ('created', models.DateTimeField(null=True, blank=True)),
                ('updated', models.DateTimeField(null=True, blank=True)),
                ('countries', models.ManyToManyField(related_name='countries', verbose_name='Accessible Countires', to='activitydb.Country', blank=True)),
                ('country', models.ForeignKey(blank=True, to='activitydb.Country', null=True)),
                ('modified_by', models.ForeignKey(related_name='userprofile_modified_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(related_name='userprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='siteprofile',
            name='classify_land',
            field=models.ForeignKey(blank=True, to='activitydb.LandType', null=True),
        ),
    ]
