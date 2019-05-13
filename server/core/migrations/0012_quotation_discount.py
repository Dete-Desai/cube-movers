# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20150902_0111'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='discount',
            field=models.FloatField(default=0.0),
        ),
    ]
