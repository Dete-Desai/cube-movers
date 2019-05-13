# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_auto_20160403_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='movetype',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='movetypedetails',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
