# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20160210_1237'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='move',
            options={'permissions': (('can_view_unassigned_move', 'Can view unassigned move'),)},
        ),
        migrations.AlterModelOptions(
            name='quotation',
            options={'permissions': (('can_view_unassigned_quote', 'Can view unassigned quote'),)},
        ),
    ]
