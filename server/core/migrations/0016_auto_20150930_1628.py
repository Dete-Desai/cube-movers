# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20150910_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='secondary_name',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='secondary_phone_number',
            field=models.CharField(max_length=30, null=True, blank=True),
        ),
    ]
