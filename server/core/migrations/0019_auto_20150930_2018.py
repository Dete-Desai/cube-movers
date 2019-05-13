# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_staffprofile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffprofile',
            name='phone_number',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
