# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-06 09:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='robot',
            name='brand',
            field=models.CharField(default='Roboticia', max_length=20),
        ),
    ]