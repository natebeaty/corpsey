# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from django.conf import settings
import easy_thumbnails.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artists', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField(blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('starter', models.BooleanField(default=False)),
                ('featured', models.BooleanField(default=False)),
                ('full_image', easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'comics', blank=True)),
                ('panel1', easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'comics', blank=True)),
                ('panel2', easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'comics', blank=True)),
                ('panel3', easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'comics', blank=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('artist', models.ForeignKey(related_name='comics', blank=True, to='artists.Artist', null=True)),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='comics.Comic', null=True)),
                ('portal_to', models.ForeignKey(related_name='portal', blank=True, to='comics.Comic', null=True)),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Contribution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, blank=True)),
                ('email', models.CharField(max_length=250, blank=True)),
                ('website', models.URLField(max_length=250, blank=True)),
                ('code', models.CharField(help_text=b'Upload link is http://corpsey.trubbleclub.com/contribute/upload/CODE_HERE/', max_length=250, blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField(blank=True)),
                ('panel1', easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'contributions', blank=True)),
                ('panel2', easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'contributions', blank=True)),
                ('panel3', easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'contributions', blank=True)),
                ('pending', models.BooleanField(default=True)),
                ('has_panels', models.BooleanField(default=False)),
                ('accepted', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
                ('comic', models.ForeignKey(related_name='contributions', to='comics.Comic')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Uturn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('panel', easy_thumbnails.fields.ThumbnailerImageField(upload_to=b'comics', blank=True)),
                ('portal_to', models.ForeignKey(related_name='uturn', to='comics.Comic')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('approve', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
                ('contribution', models.ForeignKey(related_name='votes', to='comics.Contribution')),
                ('rule_broke', models.ForeignKey(related_name='rules_broke', default=None, blank=True, to='comics.Rule', null=True)),
                ('user', models.ForeignKey(related_name='votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
