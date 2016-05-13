# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, blank=True)),
                ('first_name', models.CharField(max_length=250, blank=True)),
                ('last_name', models.CharField(max_length=250, blank=True)),
                ('email', models.CharField(max_length=250, blank=True)),
                ('url', models.URLField(max_length=250, blank=True)),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'artists', blank=True)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
            bases=(models.Model,),
        ),
    ]
