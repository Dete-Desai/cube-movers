# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_checklistitem_office'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='quote_number',
            field=models.CharField(default=b'', max_length=50),
        ),
    ]
