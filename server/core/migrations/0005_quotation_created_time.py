# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_quotation_move_rep'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='created_time',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 26, 20, 10, 6, 98120, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
