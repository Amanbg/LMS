# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-04 12:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LeadSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_name', models.CharField(max_length=20)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
    ]
