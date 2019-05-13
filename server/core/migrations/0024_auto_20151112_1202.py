# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20151112_1202'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checklistitem',
            old_name='item_foreign',
            new_name='item',
        ),
    ]
