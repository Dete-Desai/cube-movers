# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0034_auto_20160311_0100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movevehicle',
            name='move',
        ),
        migrations.RemoveField(
            model_name='movevehicle',
            name='vehicle',
        ),
        migrations.AddField(
            model_name='move',
            name='move_vehicles',
            field=models.ManyToManyField(to='core.Vehicle'),
        ),
        migrations.AlterField(
            model_name='move',
            name='move_team',
            field=models.ForeignKey(to='core.MoveTeam', null=True),
        ),
        migrations.AlterField(
            model_name='move',
            name='trainee_team',
            field=models.ForeignKey(to='core.TraineeTeam', null=True),
        ),
        migrations.AlterField(
            model_name='traineeteammember',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='MoveVehicle',
        ),
    ]
