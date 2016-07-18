# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-07-17 16:58
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tip',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('desc', models.CharField(max_length=1000)),
                ('image', models.ImageField(null=True, upload_to='tips_image/')),
                ('date', models.DateField(default=datetime.date(2016, 7, 17))),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tips', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
