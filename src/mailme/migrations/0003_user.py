# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '__first__'),
        ('mailme', '0002_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(max_length=50, verbose_name='Username', unique=True, null=True)),
                ('email', models.EmailField(max_length=254, verbose_name='Email', unique=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name', null=True, blank=True)),
                ('is_staff', models.BooleanField(verbose_name='Staff', default=False)),
                ('is_active', models.BooleanField(verbose_name='Active', default=True)),
                ('is_organization', models.BooleanField(verbose_name='Organization', default=False)),
                ('profile_url', models.URLField(max_length=2048, verbose_name='Profile', null=True, blank=True)),
                ('date_joined', models.DateTimeField(verbose_name='date joined', default=django.utils.timezone.now)),
                ('email_verified', models.BooleanField(default=False)),
                ('enable_notifications', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(verbose_name='groups', to='auth.Group', blank=True)),
                ('user_permissions', models.ManyToManyField(verbose_name='user permissions', to='auth.Permission', blank=True)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'db_table': 'mailme_user',
            },
            bases=(models.Model,),
        ),
    ]
