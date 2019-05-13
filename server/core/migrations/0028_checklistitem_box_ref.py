# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20160129_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklistitem',
            name='box_ref',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
