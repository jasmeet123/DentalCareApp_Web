# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-03 19:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserLogin', '0011_auto_20160703_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlogin',
            name='fbuserId',
            field=models.CharField(default='1', max_length=50),
        ),
    ]