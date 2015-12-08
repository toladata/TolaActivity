# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0022_documentation_program'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Name', blank=True)),
                ('title', models.CharField(max_length=255, null=True, verbose_name='Title', blank=True)),
                ('city', models.CharField(max_length=255, null=True, verbose_name='City/Town', blank=True)),
                ('address', models.TextField(max_length=255, null=True, verbose_name='Address', blank=True)),
                ('email', models.CharField(max_length=255, null=True, verbose_name='Email', blank=True)),
                ('phone', models.CharField(max_length=255, null=True, verbose_name='Phone', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('country', models.ForeignKey(to='activitydb.Country')),
            ],
            options={
                'ordering': ('country', 'name', 'title'),
                'verbose_name_plural': 'Contact',
            },
        ),
        migrations.CreateModel(
            name='Stakeholder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Stakholder/Organization Name', blank=True)),
                ('stakeholder_register', models.BooleanField(verbose_name='Has this partner been added to stakeholder register?')),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('contact', models.ManyToManyField(to='activitydb.Contact', max_length=255, blank=True)),
                ('country', models.ForeignKey(to='activitydb.Country')),
                ('formal_relationship_document', models.ForeignKey(related_name='relationship_document', verbose_name='Formal Written Description of Relationship', to='activitydb.Documentation', null=True)),
                ('sector', models.ForeignKey(blank=True, to='activitydb.Sector', null=True)),
            ],
            options={
                'ordering': ('country', 'name', 'type'),
                'verbose_name_plural': 'Stakeholders',
            },
        ),
        migrations.CreateModel(
            name='StakeholderType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name='Stakeholder Type', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('country', models.ForeignKey(to='activitydb.Country')),
            ],
            options={
                'ordering': ('country', 'name'),
                'verbose_name_plural': 'Stakeholder Types',
            },
        ),
        migrations.AddField(
            model_name='stakeholder',
            name='type',
            field=models.ForeignKey(to='activitydb.StakeholderType'),
        ),
        migrations.AddField(
            model_name='stakeholder',
            name='vetting_document',
            field=models.ForeignKey(related_name='vetting_document', verbose_name='Vetting/ due diligence statement', to='activitydb.Documentation', null=True),
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='stakeholder',
            field=models.ForeignKey(blank=True, to='activitydb.Stakeholder', null=True),
        ),
    ]
