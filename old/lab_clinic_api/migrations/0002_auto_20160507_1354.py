# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-07 13:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import edc_base.model.validators.date


class Migration(migrations.Migration):

    dependencies = [
        ('lab_clinic_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aliquot',
            name='aliquot_datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 7, 13, 53, 35, 907352), verbose_name='Date and time aliquot created'),
        ),
        migrations.AlterField(
            model_name='receive',
            name='receive_datetime',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2016, 5, 7, 13, 53, 35, 875943), validators=[edc_base.model.validators.date.datetime_not_future], verbose_name='Date and time received'),
        ),
    ]