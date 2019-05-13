# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20160205_0104'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklistitem',
            name='office',
            field=models.ForeignKey(to='core.Office', null=True),
        ),
    ]
