# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-10 16:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_auto_20170910_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='agendaitem',
            name='title',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
