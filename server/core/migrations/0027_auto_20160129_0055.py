# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_staffprofile_signature'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('branch_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='staffprofile',
            name='signature',
            field=models.ImageField(null=True, upload_to=b'signatures', blank=True),
        ),
        migrations.AddField(
            model_name='move',
            name='branch',
            field=models.ForeignKey(to='core.Branch', null=True),
        ),
    ]
