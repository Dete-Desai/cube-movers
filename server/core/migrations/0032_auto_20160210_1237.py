# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_quotation_quote_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=30),
        ),
        migrations.AlterField(
            model_name='customer',
            name='secondary_phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=30, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='staffprofile',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=50, null=True),
        ),
    ]
