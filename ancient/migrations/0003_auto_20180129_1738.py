# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-29 09:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ancient', '0002_submit_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='test_input',
            field=models.FilePathField(default='./NoAddress'),
        ),
        migrations.AddField(
            model_name='homework',
            name='test_output',
            field=models.FilePathField(default='./NoAddress'),
        ),
    ]
