# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enclosure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('url', models.URLField(verbose_name='URL')),
                ('type', models.CharField(verbose_name='type', max_length=200)),
                ('length', models.PositiveIntegerField(verbose_name='length', default=0)),
            ],
            options={
                'verbose_name': 'enclosure',
                'verbose_name_plural': 'enclosures',
                'db_table': 'mailme_enclosure',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='title', max_length=200)),
                ('domain', models.CharField(verbose_name='domain', blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'category',
                'unique_together': set([('title', 'domain')]),
                'verbose_name_plural': 'categories',
                'db_table': 'mailme_category',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('username', models.CharField(verbose_name='Username', max_length=50, unique=True, null=True)),
                ('email', models.EmailField(verbose_name='Email', max_length=254, unique=True)),
                ('name', models.CharField(verbose_name='Name', blank=True, max_length=100, null=True)),
                ('is_staff', models.BooleanField(verbose_name='staff status', help_text='Designates whether the user can log into this admin site.', default=False)),
                ('is_active', models.BooleanField(verbose_name='active', help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', default=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('email_verified', models.BooleanField(default=False)),
                ('enable_notifications', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'mailme_user',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.TextField(verbose_name='title')),
                ('feed_url', models.URLField(verbose_name='feed URL', max_length=2048, unique=True)),
                ('description', models.TextField(verbose_name='description')),
                ('link', models.URLField(verbose_name='link', blank=True, max_length=2048)),
                ('http_etag', models.CharField(verbose_name='E-Tag', blank=True, max_length=200, editable=False, null=True)),
                ('http_last_modified', models.DateTimeField(verbose_name='Last-Modified', blank=True, editable=False, null=True)),
                ('date_last_refresh', models.DateTimeField(verbose_name='date of last refresh', blank=True, editable=False, null=True)),
                ('last_error', models.CharField(verbose_name='last error', blank=True, choices=[('TIMEDOUT_ERROR', 'The feed does not seem to be respond. We will try again later.'), ('NOT_FOUND_ERROR', 'You entered an incorrect URL or the feed you requested does not exist anymore.'), ('GENERIC_ERROR', 'There was a problem with the feed you provided, please check the URL for mispellings or try again later.')], max_length=32, default='')),
                ('date_created', models.DateTimeField(verbose_name='date created', auto_now_add=True)),
                ('date_changed', models.DateTimeField(verbose_name='date changed', auto_now=True)),
                ('is_active', models.BooleanField(verbose_name='is active', default=True)),
                ('freq', models.IntegerField(verbose_name='frequency', default=10800)),
                ('categories', models.ManyToManyField(to='mailme.Category')),
            ],
            options={
                'verbose_name': 'syndication feed',
                'ordering': ('id',),
                'verbose_name_plural': 'syndication feeds',
                'db_table': 'mailme_feed',
            },
            bases=(models.Model,),
        ),
    ]
