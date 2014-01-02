# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Category', fields ['name', 'domain']
        db.delete_unique('core_category', ['name', 'domain'])

        # Deleting field 'Category.name'
        db.delete_column('core_category', 'name')

        # Adding field 'Category.title'
        db.add_column('core_category', 'title',
                      self.gf('django.db.models.fields.CharField')(max_length=200, default=''),
                      keep_default=False)

        # Adding unique constraint on 'Category', fields ['title', 'domain']
        db.create_unique('core_category', ['title', 'domain'])

        # Deleting field 'Feed.name'
        db.delete_column('core_feed', 'name')

        # Adding field 'Feed.title'
        db.add_column('core_feed', 'title',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'Category', fields ['title', 'domain']
        db.delete_unique('core_category', ['title', 'domain'])

        # Adding field 'Category.name'
        db.add_column('core_category', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=200, default=''),
                      keep_default=False)

        # Deleting field 'Category.title'
        db.delete_column('core_category', 'title')

        # Adding unique constraint on 'Category', fields ['name', 'domain']
        db.create_unique('core_category', ['name', 'domain'])

        # Adding field 'Feed.name'
        db.add_column('core_feed', 'name',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Deleting field 'Feed.title'
        db.delete_column('core_feed', 'title')


    models = {
        'core.category': {
            'Meta': {'object_name': 'Category', 'unique_together': "(('title', 'domain'),)"},
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
            'Meta': {'object_name': 'Feed', 'ordering': "('id',)"},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Category']"}),
            'date_changed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_refresh': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'feed_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '2048'}),
            'freq': ('django.db.models.fields.IntegerField', [], {'default': '10800'}),
            'http_etag': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '200'}),
            'http_last_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_error': ('django.db.models.fields.CharField', [], {'max_length': '32', 'default': "''", 'blank': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {})
        },
        'core.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Category']"}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enclosures': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'blank': 'True', 'to': "orm['core.Enclosure']"}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Feed']"}),
            'guid': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'blank': 'True'}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_organization': ('django.db.models.fields.BooleanField', [], {}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'profile_url': ('django.db.models.fields.URLField', [], {'null': 'True', 'blank': 'True', 'max_length': '2048'}),
            'username': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['core']