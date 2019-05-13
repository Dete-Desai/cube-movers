# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_checklistitem_box_ref'),
    ]

    operations = [
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('office_name', models.CharField(unique=True, max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='room_type',
            field=models.CharField(default=b'house', max_length=50, choices=[(b'office', b'office'), (b'house', b'house')]),
        ),
    ]
