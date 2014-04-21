# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Post.date_published'
        db.delete_column('core_post', 'date_published')

        # Deleting field 'Post.date_updated'
        db.delete_column('core_post', 'date_updated')

        # Adding field 'Post.published'
        db.add_column('core_post', 'published',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Post.updated'
        db.add_column('core_post', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)


        # Changing field 'Post.author'
        db.alter_column('core_post', 'author', self.gf('django.db.models.fields.TextField')())

        # Changing field 'Feed.name'
        db.alter_column('core_feed', 'name', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):
        # Adding field 'Post.date_published'
        db.add_column('core_post', 'date_published',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 2, 0, 0)),
                      keep_default=False)

        # Adding field 'Post.date_updated'
        db.add_column('core_post', 'date_updated',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 2, 0, 0)),
                      keep_default=False)

        # Deleting field 'Post.published'
        db.delete_column('core_post', 'published')

        # Deleting field 'Post.updated'
        db.delete_column('core_post', 'updated')


        # Changing field 'Post.author'
        db.alter_column('core_post', 'author', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Feed.name'
        db.alter_column('core_feed', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))

    models = {
        'core.category': {
            'Meta': {'object_name': 'Category', 'unique_together': "(('name', 'domain'),)"},
            'domain': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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
            'date_changed': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'date_last_refresh': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'feed_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '2048'}),
            'freq': ('django.db.models.fields.IntegerField', [], {'default': '10800'}),
            'http_etag': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'http_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_error': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '32', 'default': "''"}),
            'link': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '2048'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'core.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['core.Category']"}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'enclosures': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'symmetrical': 'False', 'to': "orm['core.Enclosure']"}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_organization': ('django.db.models.fields.BooleanField', [], {}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '100'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'profile_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'null': 'True', 'max_length': '2048'}),
            'username': ('django.db.models.fields.CharField', [], {'null': 'True', 'max_length': '50'})
        }
    }

    complete_apps = ['core']
