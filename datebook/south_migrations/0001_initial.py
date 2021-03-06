# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Datebook'
        db.create_table(u'datebook_datebook', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('period', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'datebook', ['Datebook'])

        # Adding unique constraint on 'Datebook', fields ['author', 'period']
        db.create_unique(u'datebook_datebook', ['author_id', 'period'])

        # Adding model 'DayEntry'
        db.create_table(u'datebook_dayentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('datebook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['datebook.Datebook'])),
            ('activity_date', self.gf('django.db.models.fields.DateField')()),
            ('vacation', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('content', self.gf('django.db.models.fields.TextField')(max_length=500, blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('stop', self.gf('django.db.models.fields.DateTimeField')()),
            ('pause', self.gf('django.db.models.fields.TimeField')(default=datetime.time(0, 0))),
        ))
        db.send_create_signal(u'datebook', ['DayEntry'])

        # Adding unique constraint on 'DayEntry', fields ['datebook', 'activity_date']
        db.create_unique(u'datebook_dayentry', ['datebook_id', 'activity_date'])


    def backwards(self, orm):
        # Removing unique constraint on 'DayEntry', fields ['datebook', 'activity_date']
        db.delete_unique(u'datebook_dayentry', ['datebook_id', 'activity_date'])

        # Removing unique constraint on 'Datebook', fields ['author', 'period']
        db.delete_unique(u'datebook_datebook', ['author_id', 'period'])

        # Deleting model 'Datebook'
        db.delete_table(u'datebook_datebook')

        # Deleting model 'DayEntry'
        db.delete_table(u'datebook_dayentry')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'datebook.datebook': {
            'Meta': {'unique_together': "(('author', 'period'),)", 'object_name': 'Datebook'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'period': ('django.db.models.fields.DateField', [], {})
        },
        u'datebook.dayentry': {
            'Meta': {'unique_together': "(('datebook', 'activity_date'),)", 'object_name': 'DayEntry'},
            'activity_date': ('django.db.models.fields.DateField', [], {}),
            'content': ('django.db.models.fields.TextField', [], {'max_length': '500', 'blank': 'True'}),
            'datebook': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['datebook.Datebook']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pause': ('django.db.models.fields.TimeField', [], {'default': 'datetime.time(0, 0)'}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'stop': ('django.db.models.fields.DateTimeField', [], {}),
            'vacation': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['datebook']