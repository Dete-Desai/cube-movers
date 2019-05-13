# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_quotedocument'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffprofile',
            name='signature',
            field=models.ImageField(null=True, upload_to=b'signatures'),
        ),
    ]
