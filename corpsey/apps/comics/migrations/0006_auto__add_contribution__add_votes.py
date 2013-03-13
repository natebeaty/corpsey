# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Contribution'
        db.create_table('comics_contribution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('comic', self.gf('django.db.models.fields.related.ForeignKey')(related_name='contributions', to=orm['comics.Comic'])),
            ('panel1', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('panel2', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('panel3', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('comics', ['Contribution'])

        # Adding model 'Votes'
        db.create_table('comics_votes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('contribution', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['comics.Contribution'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['auth.User'])),
        ))
        db.send_create_signal('comics', ['Votes'])


    def backwards(self, orm):
        # Deleting model 'Contribution'
        db.delete_table('comics_contribution')

        # Deleting model 'Votes'
        db.delete_table('comics_votes')


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
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
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
        'comics.contribution': {
            'Meta': {'object_name': 'Contribution'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'comic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'contributions'", 'to': "orm['comics.Comic']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'panel1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'panel2': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'panel3': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'})
        },
        'comics.uturn': {
            'Meta': {'object_name': 'Uturn'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'panel': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'portal_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'uturn'", 'to': "orm['comics.Comic']"})
        },
        'comics.votes': {
            'Meta': {'object_name': 'Votes'},
            'contribution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': "orm['comics.Contribution']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['comics']