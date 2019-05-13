# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0017_staffprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffprofile',
            name='user',
            field=models.OneToOneField(default=None, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
