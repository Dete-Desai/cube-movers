# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20160224_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='MoveTypeDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='move',
            name='move_type_details',
            field=models.ForeignKey(to='core.MoveTypeDetails', null=True),
        ),
    ]
