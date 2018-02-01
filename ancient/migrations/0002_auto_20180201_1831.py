# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-01 10:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ancient', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='homework',
            name='test_input',
            field=models.TextField(default='./NoHomewr\x08ork'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='homework',
            name='test_output',
            field=models.TextField(default='./NoHomeWork'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submit',
            name='score',
            field=models.CharField(default='Not Run yet', max_length=10),
        ),
    ]
