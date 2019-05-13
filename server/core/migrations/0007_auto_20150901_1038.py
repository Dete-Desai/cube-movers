# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_movelogs_move_rep'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='reply_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='quotation',
            name='sent_time',
            field=models.DateTimeField(null=True),
        ),
    ]
