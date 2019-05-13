# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='move',
            name='move_rep',
            field=models.ForeignKey(related_name='move_rep', to=settings.AUTH_USER_MODEL),
        ),
    ]
