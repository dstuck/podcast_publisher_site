# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 05:36
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sermon_storer', '0003_auto_20171105_2304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sermon',
            old_name='filename',
            new_name='preacher',
        ),
    ]
