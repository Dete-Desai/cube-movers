# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Checklist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_vol', models.FloatField(default=0.0, null=True)),
                ('total_cost', models.FloatField(default=0.0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChecklistItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.CharField(max_length=30)),
                ('vol', models.FloatField()),
                ('qty', models.IntegerField(default=0, null=True)),
                ('is_packed', models.BooleanField(default=False)),
                ('is_unpacked', models.BooleanField(default=False)),
                ('checklist', models.ForeignKey(to='core.Checklist')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('full_name', models.CharField(max_length=50)),
                ('secondary_name', models.CharField(max_length=50, blank=True)),
                ('phone_number', models.CharField(max_length=30)),
                ('secondary_phone_number', models.CharField(max_length=30, blank=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Delight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('smartness', models.IntegerField(null=True)),
                ('time', models.IntegerField(null=True)),
                ('courtesy', models.IntegerField(null=True)),
                ('creativity', models.IntegerField(null=True)),
                ('explanation', models.IntegerField(null=True)),
                ('willingness', models.IntegerField(null=True)),
                ('leader_competence', models.IntegerField(null=True)),
                ('team_competence', models.IntegerField(null=True)),
                ('care_attention', models.IntegerField(null=True)),
                ('satisfaction', models.IntegerField(null=True)),
                ('comments', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('vol', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Move',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hash', models.TextField(null=True)),
                ('token', models.CharField(max_length=10, null=True)),
                ('is_credit', models.BooleanField(default=False)),
                ('move_date', models.DateTimeField(null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('customer', models.ForeignKey(to='core.Customer')),
                ('delight', models.OneToOneField(null=True, to='core.Delight')),
                ('move_rep', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MoveLogs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('move', models.ForeignKey(to='core.Move', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MoveStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='MoveTeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='MoveTeamMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_lead', models.BooleanField(default=False)),
                ('move_team', models.ForeignKey(to='core.MoveTeam')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MoveType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('currency', models.CharField(default=b'KES', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='MoveVehicle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('move', models.ForeignKey(to='core.Move')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyDetails',
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
        migrations.CreateModel(
            name='Quotation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('total_cost', models.FloatField(default=0.0, null=True)),
                ('profit_margin', models.FloatField(default=0.0, null=True)),
                ('commission', models.FloatField(default=0.0, null=True)),
                ('selling_price', models.FloatField(default=0.0, null=True)),
                ('vat', models.FloatField(default=16.0, null=True)),
                ('charge_out_price', models.FloatField(default=0.0, null=True)),
                ('hash', models.TextField(null=True)),
                ('status', models.CharField(default=b'not sent', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='QuoteItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.CharField(max_length=30)),
                ('cost', models.FloatField()),
                ('units', models.IntegerField()),
                ('quotation', models.ForeignKey(to='core.Quotation')),
            ],
        ),
        migrations.CreateModel(
            name='QuoteItemDefault',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('item', models.CharField(unique=True, max_length=30)),
                ('cost', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='QuoteItemType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('survey_time', models.DateTimeField(null=True)),
                ('move_time', models.DateTimeField(null=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('surveyor', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TraineeTeam',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='TraineeTeamMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('trainee_team', models.ForeignKey(to='core.TraineeTeam')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('make', models.CharField(max_length=30)),
                ('model', models.CharField(max_length=30)),
                ('registration', models.CharField(max_length=30)),
                ('cbm', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='survey',
            name='vehicle',
            field=models.ForeignKey(to='core.Vehicle', null=True),
        ),
        migrations.AddField(
            model_name='quoteitemdefault',
            name='quote_item_type',
            field=models.ForeignKey(to='core.QuoteItemType', null=True),
        ),
        migrations.AddField(
            model_name='quoteitem',
            name='quote_item_type',
            field=models.ForeignKey(to='core.QuoteItemType', null=True),
        ),
        migrations.AddField(
            model_name='movevehicle',
            name='vehicle',
            field=models.OneToOneField(to='core.Vehicle'),
        ),
        migrations.AddField(
            model_name='movelogs',
            name='move_status',
            field=models.ForeignKey(to='core.MoveStatus', null=True),
        ),
        migrations.AddField(
            model_name='move',
            name='move_status',
            field=models.ForeignKey(to='core.MoveStatus'),
        ),
        migrations.AddField(
            model_name='move',
            name='move_team',
            field=models.OneToOneField(null=True, to='core.MoveTeam'),
        ),
        migrations.AddField(
            model_name='move',
            name='move_type',
            field=models.ForeignKey(to='core.MoveType', null=True),
        ),
        migrations.AddField(
            model_name='move',
            name='property_details',
            field=models.OneToOneField(to='core.PropertyDetails'),
        ),
        migrations.AddField(
            model_name='move',
            name='survey',
            field=models.OneToOneField(to='core.Survey'),
        ),
        migrations.AddField(
            model_name='move',
            name='trainee_team',
            field=models.OneToOneField(null=True, to='core.TraineeTeam'),
        ),
        migrations.AddField(
            model_name='customer',
            name='source',
            field=models.ForeignKey(to='core.Source'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='checklistitem',
            name='room',
            field=models.ForeignKey(to='core.Room'),
        ),
        migrations.AddField(
            model_name='checklist',
            name='move',
            field=models.OneToOneField(to='core.Move'),
        ),
        migrations.AddField(
            model_name='checklist',
            name='quotation',
            field=models.OneToOneField(null=True, to='core.Quotation'),
        ),
    ]
