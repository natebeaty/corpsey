# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Uturn'
        db.create_table('comics_uturn', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('portal_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='uturn', to=orm['comics.Comic'])),
            ('panel', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('comics', ['Uturn'])


    def backwards(self, orm):
        # Deleting model 'Uturn'
        db.delete_table('comics_uturn')


    models = {
        'artists.artist': {
            'Meta': {'ordering': "['last_name', 'first_name']", 'object_name': 'Artist'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        'comics.comic': {
            'Meta': {'ordering': "['tree_id', 'lft']", 'object_name': 'Comic'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'artists'", 'null': 'True', 'to': "orm['artists.Artist']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'full_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'panel1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'panel2': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'panel3': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['comics.Comic']"}),
            'portal_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'portal'", 'null': 'True', 'to': "orm['comics.Comic']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'starter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'comics.uturn': {
            'Meta': {'object_name': 'Uturn'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'panel': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'portal_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'uturn'", 'to': "orm['comics.Comic']"})
        }
    }

    complete_apps = ['comics']