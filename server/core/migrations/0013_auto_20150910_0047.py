# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_quotation_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='move',
            name='arrival_at_office',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='move',
            name='arrive_at_client',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='move',
            name='departure_from_client',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='move',
            name='departure_from_office',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='move',
            name='fuel_intake',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='move',
            name='kms_run',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='move',
            name='speedometer_in',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='move',
            name='speedometer_out',
            field=models.FloatField(null=True),
        ),
    ]
