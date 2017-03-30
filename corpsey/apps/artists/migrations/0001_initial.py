# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-30 01:52
from __future__ import unicode_literals

from django.db import migrations, models
import easy_thumbnails.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250)),
                ('first_name', models.CharField(blank=True, max_length=250)),
                ('last_name', models.CharField(blank=True, max_length=250)),
                ('email', models.CharField(blank=True, max_length=250)),
                ('url', models.URLField(blank=True, max_length=250)),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(blank=True, upload_to=b'artists')),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
    ]
