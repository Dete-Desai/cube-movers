# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_checklistitem_item_foreign'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checklistitem',
            old_name='item',
            new_name='item_backup',
        ),
    ]
