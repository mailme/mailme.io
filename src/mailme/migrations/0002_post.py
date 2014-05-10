# encoding: utf8
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
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('feed', models.ForeignKey(to='mailme.Feed', to_field='id')),
                ('title', models.TextField(verbose_name='title')),
                ('link', models.URLField(max_length=2048, verbose_name='link')),
                ('content', models.TextField(blank=True, verbose_name='content')),
                ('guid', models.CharField(max_length=2048, blank=True, verbose_name='guid')),
                ('author', models.TextField(blank=True, verbose_name='author')),
                ('published', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published')),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date updated')),
                ('enclosures', models.ManyToManyField(to='mailme.Enclosure', blank=True)),
                ('categories', models.ManyToManyField(to='mailme.Category')),
            ],
            options={
                'verbose_name_plural': 'posts',
                'verbose_name': 'post',
            },
            bases=(models.Model,),
        ),
    ]
