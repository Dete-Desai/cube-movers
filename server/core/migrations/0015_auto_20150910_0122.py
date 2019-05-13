# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20150910_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='fuel_intake',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='move',
            name='kms_run',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='move',
            name='speedometer_in',
            field=models.FloatField(default=0.0, null=True),
        ),
        migrations.AlterField(
            model_name='move',
            name='speedometer_out',
            field=models.FloatField(default=0.0, null=True),
        ),
    ]
