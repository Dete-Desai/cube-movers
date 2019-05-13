# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_auto_20160420_0040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='move',
            name='kms_run',
        ),
    ]
