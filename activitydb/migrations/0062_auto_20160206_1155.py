# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activitydb', '0061_auto_20160202_0706'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TolaUser',
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
                ('modified_by', models.ForeignKey(related_name='tola_mod', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(related_name='tola_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
