# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20150901_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='delight',
            name='total',
            field=models.IntegerField(null=True),
        ),
    ]
