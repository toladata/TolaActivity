# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0042_auto_20151030_1237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stakeholder',
            name='formal_relationship_document',
            field=models.ForeignKey(related_name='relationship_document', verbose_name='Formal Written Description of Relationship', blank=True, to='activitydb.Documentation', null=True),
        ),
        migrations.AlterField(
            model_name='stakeholder',
            name='type',
            field=models.ForeignKey(blank=True, to='activitydb.StakeholderType', null=True),
        ),
        migrations.AlterField(
            model_name='stakeholder',
            name='vetting_document',
            field=models.ForeignKey(related_name='vetting_document', verbose_name='Vetting/ due diligence statement', blank=True, to='activitydb.Documentation', null=True),
        ),
    ]
