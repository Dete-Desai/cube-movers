# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20150902_0019'),
    ]

    operations = [
        migrations.AddField(
            model_name='move',
            name='accessibility_instructions',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='move',
            name='special_instructions',
            field=models.TextField(null=True),
        ),
    ]
