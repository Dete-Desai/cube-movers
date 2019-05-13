# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20150930_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffprofile',
            name='code',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
