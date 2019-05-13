# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_room_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklistitem',
            name='item_foreign',
            field=models.ForeignKey(blank=True, to='core.Item', null=True),
        ),
    ]
