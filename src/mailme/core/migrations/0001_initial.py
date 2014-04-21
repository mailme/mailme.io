# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('core_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('domain', self.gf('django.db.models.fields.CharField')(blank=True, null=True, max_length=128)),
        ))
        db.send_create_signal('core', ['Category'])

        # Adding unique constraint on 'Category', fields ['name', 'domain']
        db.create_unique('core_category', ['name', 'domain'])

        # Adding model 'Feed'
        db.create_table('core_feed', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('feed_url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('link', self.gf('django.db.models.fields.URLField')(blank=True, max_length=200)),
            ('http_etag', self.gf('django.db.models.fields.CharField')(blank=True, null=True, max_length=200)),
            ('http_last_modified', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True)),
            ('date_last_refresh', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True)),
            ('last_error', self.gf('django.db.models.fields.CharField')(blank=True, default='', max_length=32)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_changed', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('freq', self.gf('django.db.models.fields.IntegerField')(default=10800)),
        ))
        db.send_create_signal('core', ['Feed'])

        # Adding M2M table for field categories on 'Feed'
        m2m_table_name = db.shorten_name('core_feed_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('feed', models.ForeignKey(orm['core.feed'], null=False)),
            ('category', models.ForeignKey(orm['core.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['feed_id', 'category_id'])

        # Adding model 'Enclosure'
        db.create_table('core_enclosure', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('length', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('core', ['Enclosure'])

        # Adding model 'Post'
        db.create_table('core_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Feed'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=2048)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('guid', self.gf('django.db.models.fields.CharField')(blank=True, max_length=200)),
            ('author', self.gf('django.db.models.fields.CharField')(blank=True, max_length=50)),
            ('date_published', self.gf('django.db.models.fields.DateField')()),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('core', ['Post'])

        # Adding M2M table for field enclosures on 'Post'
        m2m_table_name = db.shorten_name('core_post_enclosures')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm['core.post'], null=False)),
            ('enclosure', models.ForeignKey(orm['core.enclosure'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'enclosure_id'])

        # Adding M2M table for field categories on 'Post'
        m2m_table_name = db.shorten_name('core_post_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm['core.post'], null=False)),
            ('category', models.ForeignKey(orm['core.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'category_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Category', fields ['name', 'domain']
        db.delete_unique('core_category', ['name', 'domain'])

        # Deleting model 'Category'
        db.delete_table('core_category')

        # Deleting model 'Feed'
        db.delete_table('core_feed')

        # Removing M2M table for field categories on 'Feed'
        db.delete_table(db.shorten_name('core_feed_categories'))

        # Deleting model 'Enclosure'
        db.delete_table('core_enclosure')

        # Deleting model 'Post'
        db.delete_table('core_post')

        # Removing M2M table for field enclosures on 'Post'
        db.delete_table(db.shorten_name('core_post_enclosures'))

        # Removing M2M table for field categories on 'Post'
        db.delete_table(db.shorten_name('core_post_categories'))


    models = {
        'core.category': {
            'Meta': {'unique_together': "(('name', 'domain'),)", 'object_name': 'Category'},
            'domain': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
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
            'date_changed': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_refresh': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'feed_url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'freq': ('django.db.models.fields.IntegerField', [], {'default': '10800'}),
            'http_etag': ('django.db.models.fields.CharField', [], {'blank': 'True', 'null': 'True', 'max_length': '200'}),
            'http_last_modified': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_error': ('django.db.models.fields.CharField', [], {'blank': 'True', 'default': "''", 'max_length': '32'}),
            'link': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'core.post': {
            'Meta': {'object_name': 'Post'},
            'author': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '50'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Category']", 'symmetrical': 'False'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_published': ('django.db.models.fields.DateField', [], {}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {}),
            'enclosures': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Enclosure']", 'blank': 'True', 'symmetrical': 'False'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Feed']"}),
            'guid': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '2048'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['core']
