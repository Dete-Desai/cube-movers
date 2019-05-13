# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20150910_0047'),
    ]

    operations = [
        migrations.RenameField(
            model_name='move',
            old_name='arrive_at_client',
            new_name='arrival_at_client',
        ),
    ]
