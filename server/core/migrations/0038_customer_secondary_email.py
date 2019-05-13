# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_remove_move_kms_run'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='secondary_email',
            field=models.EmailField(max_length=254, null=True, blank=True),
        ),
    ]
