# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-03 01:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hadiths', '0005_make_fields_nullable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hadith',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='hadiths', to='hadiths.Person'),
        ),
    ]
