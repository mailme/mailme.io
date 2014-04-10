# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'User.email_verified'
        db.add_column('core_user', 'email_verified',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'User.enable_notifications'
        db.add_column('core_user', 'enable_notifications',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding unique constraint on 'User', fields ['username']
        db.create_unique('core_user', ['username'])


    def backwards(self, orm):
        # Removing unique constraint on 'User', fields ['username']
        db.delete_unique('core_user', ['username'])

        # Deleting field 'User.email_verified'
        db.delete_column('core_user', 'email_verified')

        # Deleting field 'User.enable_notifications'
        db.delete_column('core_user', 'enable_notifications')


    models = {
        'core.category': {
            'Meta': {'unique_together': "(('title', 'domain'),)", 'object_name': 'Category'},
            'domain': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.enclosure': {
            'Meta': {'object_name': 'Enclosure'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'core.feed': {
            'Meta': {'ordering': "('id',)", 'object_name': 'Feed'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Category']", 'symmetrical': 'False'}),
            'date_changed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_refresh': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'feed_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '2048'}),
            'freq': ('django.db.models.fields.IntegerField', [], {'default': '10800'}),
            'http_etag': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'http_last_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_error': ('django.db.models.fields.CharField', [], {'default': "''", 'blank': 'True', 'max_length': '32'}),
            'link': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '2048'}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        'core.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Category']", 'symmetrical': 'False'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enclosures': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Enclosure']", 'blank': 'True', 'symmetrical': 'False'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Feed']"}),
            'guid': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '2048'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '2048'}),
            'published': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'core.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'email_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enable_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_organization': ('django.db.models.fields.BooleanField', [], {}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'profile_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'blank': 'True', 'max_length': '2048'}),
            'username': ('django.db.models.fields.CharField', [], {'null': 'True', 'unique': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['core']