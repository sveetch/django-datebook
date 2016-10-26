# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Datebook',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(verbose_name='created', editable=False, blank=True)),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='last edit')),
                ('period', models.DateField(verbose_name='month of activity')),
                ('notes', models.TextField(max_length=500, verbose_name='content', blank=True)),
                ('author', models.ForeignKey(verbose_name='author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Datebook',
                'verbose_name_plural': 'Datebooks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DayEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(max_length=500, verbose_name='content', blank=True)),
                ('start', models.DateTimeField(verbose_name='start')),
                ('stop', models.DateTimeField(verbose_name='stop')),
                ('pause', models.TimeField(default=datetime.time(0, 0), verbose_name='pause')),
                ('overtime', models.TimeField(default=datetime.time(0, 0), verbose_name='overtime')),
                ('activity_date', models.DateField(verbose_name='activity day date')),
                ('vacation', models.BooleanField(default=False, verbose_name='vacation')),
                ('datebook', models.ForeignKey(verbose_name='datebook', to='datebook.Datebook')),
            ],
            options={
                'verbose_name': 'day entry',
                'verbose_name_plural': 'day entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DayModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(max_length=500, verbose_name='content', blank=True)),
                ('start', models.DateTimeField(verbose_name='start')),
                ('stop', models.DateTimeField(verbose_name='stop')),
                ('pause', models.TimeField(default=datetime.time(0, 0), verbose_name='pause')),
                ('overtime', models.TimeField(default=datetime.time(0, 0), verbose_name='overtime')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('author', models.ForeignKey(verbose_name='author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'day model',
                'verbose_name_plural': 'day models',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='daymodel',
            unique_together=set([('author', 'title')]),
        ),
        migrations.AlterUniqueTogether(
            name='dayentry',
            unique_together=set([('datebook', 'activity_date')]),
        ),
        migrations.AlterUniqueTogether(
            name='datebook',
            unique_together=set([('author', 'period')]),
        ),
    ]
