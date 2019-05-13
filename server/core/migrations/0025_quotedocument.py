# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20151112_1202'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuoteDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quote_content', models.TextField()),
                ('move', models.OneToOneField(to='core.Move')),
            ],
        ),
    ]
