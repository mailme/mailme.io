# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mailme', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('feed', models.ForeignKey(to='mailme.Feed', to_field='id')),
                ('title', models.TextField(verbose_name='title')),
                ('link', models.URLField(verbose_name='link', max_length=2048)),
                ('content', models.TextField(verbose_name='content', blank=True)),
                ('guid', models.CharField(verbose_name='guid', max_length=2048, blank=True)),
                ('author', models.TextField(verbose_name='author', blank=True)),
                ('published', models.DateTimeField(verbose_name='date published', default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(verbose_name='date updated', default=django.utils.timezone.now)),
                ('enclosures', models.ManyToManyField(to='mailme.Enclosure', blank=True)),
                ('categories', models.ManyToManyField(to='mailme.Category')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
            },
            bases=(models.Model,),
        ),
    ]
