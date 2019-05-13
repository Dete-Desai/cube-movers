# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20150812_1901'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='reject_reason',
            field=models.TextField(null=True),
        ),
    ]
