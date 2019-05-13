# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_settings'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyDestinationDetails',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('primary_area_name', models.CharField(max_length=30, null=True)),
                ('secondary_area_name', models.CharField(max_length=30, null=True)),
                ('street_name', models.CharField(max_length=30, null=True)),
                ('secondary_street_name', models.CharField(max_length=30, null=True)),
                ('gate_color', models.CharField(max_length=30, null=True)),
                ('compound_name', models.CharField(max_length=30, null=True)),
                ('house_no', models.CharField(max_length=30, null=True)),
                ('floor', models.CharField(max_length=30, null=True)),
                ('land_marks', models.CharField(max_length=30, null=True)),
                ('side_of_road', models.CharField(max_length=30, null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AddField(
            model_name='move',
            name='property_destination_details',
            field=models.OneToOneField(null=True, to='core.PropertyDestinationDetails'),
        ),
    ]
