# -*- coding: utf-8 -*-
# Generated by Django 1.9.dev20150906080247 on 2015-09-23 17:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('opencivicdata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='billdocumentlink',
            name='text',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='billversionlink',
            name='text',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='eventagendamedialink',
            name='text',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='eventdocument',
            name='text',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='eventdocumentlink',
            name='text',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='eventmedialink',
            name='text',
            field=models.TextField(default=''),
        ),
    ]
