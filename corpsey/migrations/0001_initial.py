# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FlatPageMeta'
        db.create_table('flatpages_x_flatpagemeta', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flatpage', self.gf('django.db.models.fields.related.OneToOneField')(related_name='metadata', unique=True, to=orm['flatpages.FlatPage'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('flatpages_x', ['FlatPageMeta'])

        # Adding model 'FlatPageImage'
        db.create_table('flatpages_x_flatpageimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flatpage', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['flatpages.FlatPage'])),
            ('image_path', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
        ))
        db.send_create_signal('flatpages_x', ['FlatPageImage'])

        # Adding model 'Revision'
        db.create_table('flatpages_x_revision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('flatpage', self.gf('django.db.models.fields.related.ForeignKey')(related_name='revisions', to=orm['flatpages.FlatPage'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=90)),
            ('content_source', self.gf('django.db.models.fields.TextField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('view_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('flatpages_x', ['Revision'])


    def backwards(self, orm):
        # Deleting model 'FlatPageMeta'
        db.delete_table('flatpages_x_flatpagemeta')

        # Deleting model 'FlatPageImage'
        db.delete_table('flatpages_x_flatpageimage')

        # Deleting model 'Revision'
        db.delete_table('flatpages_x_revision')


    models = {
        'flatpages.flatpage': {
            'Meta': {'ordering': "('url',)", 'object_name': 'FlatPage', 'db_table': "'django_flatpage'"},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sites.Site']", 'symmetrical': 'False'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '70', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'flatpages_x.flatpageimage': {
            'Meta': {'object_name': 'FlatPageImage'},
            'flatpage': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['flatpages.FlatPage']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_path': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'})
        },
        'flatpages_x.flatpagemeta': {
            'Meta': {'object_name': 'FlatPageMeta'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'flatpage': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'metadata'", 'unique': 'True', 'to': "orm['flatpages.FlatPage']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'flatpages_x.revision': {
            'Meta': {'object_name': 'Revision'},
            'content_source': ('django.db.models.fields.TextField', [], {}),
            'flatpage': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'revisions'", 'to': "orm['flatpages.FlatPage']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '90'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'view_count': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['flatpages_x']