# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-14 05:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='leads.Lead'),
        ),
    ]
