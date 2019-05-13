# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_staffprofile_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='items',
            field=models.ManyToManyField(to='core.Item'),
        ),
    ]
