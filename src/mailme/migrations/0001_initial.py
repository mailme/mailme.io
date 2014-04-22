# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('domain', models.CharField(max_length=200, null=True, blank=True, verbose_name='domain')),
            ],
            options={
                'unique_together': set([('title', 'domain')]),
                'verbose_name_plural': 'categories',
                'verbose_name': 'category',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Enclosure',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('url', models.URLField(verbose_name='URL')),
                ('type', models.CharField(max_length=200, verbose_name='type')),
                ('length', models.PositiveIntegerField(default=0, verbose_name='length')),
            ],
            options={
                'verbose_name_plural': 'enclosures',
                'verbose_name': 'enclosure',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('username', models.CharField(max_length=50, null=True, verbose_name='Username', unique=True)),
                ('email', models.EmailField(max_length=254, verbose_name='Email', unique=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True, verbose_name='Name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email_verified', models.BooleanField(default=False)),
                ('enable_notifications', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Users',
                'verbose_name': 'User',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.TextField(verbose_name='title')),
                ('feed_url', models.URLField(max_length=2048, verbose_name='feed URL', unique=True)),
                ('description', models.TextField(verbose_name='description')),
                ('link', models.URLField(max_length=2048, blank=True, verbose_name='link')),
                ('http_etag', models.CharField(max_length=200, null=True, blank=True, verbose_name='E-Tag', editable=False)),
                ('http_last_modified', models.DateTimeField(null=True, editable=False, blank=True, verbose_name='Last-Modified')),
                ('date_last_refresh', models.DateTimeField(null=True, editable=False, blank=True, verbose_name='date of last refresh')),
                ('last_error', models.CharField(max_length=32, default='', blank=True, verbose_name='last error', choices=[('TIMEDOUT_ERROR', 'The feed does not seem to be respond. We will try again later.'), ('NOT_FOUND_ERROR', 'You entered an incorrect URL or the feed you requested does not exist anymore.'), ('GENERIC_ERROR', 'There was a problem with the feed you provided, please check the URL for mispellings or try again later.')])),
                ('date_created', models.DateTimeField(verbose_name='date created', auto_now_add=True)),
                ('date_changed', models.DateTimeField(auto_now=True, verbose_name='date changed')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('freq', models.IntegerField(default=10800, verbose_name='frequency')),
                ('categories', models.ManyToManyField(to='mailme.Category')),
            ],
            options={
                'verbose_name_plural': 'syndication feeds',
                'ordering': ('id',),
                'verbose_name': 'syndication feed',
            },
            bases=(models.Model,),
        ),
    ]
