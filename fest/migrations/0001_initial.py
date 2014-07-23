# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Item'
        db.create_table(u'fest_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('is_result_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'fest', ['Item'])

        # Adding model 'Student'
        db.create_table(u'fest_student', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('school', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('schoolcode', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('std', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'fest', ['Student'])

        # Adding M2M table for field items on 'Student'
        m2m_table_name = db.shorten_name(u'fest_student_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('student', models.ForeignKey(orm[u'fest.student'], null=False)),
            ('item', models.ForeignKey(orm[u'fest.item'], null=False))
        ))
        db.create_unique(m2m_table_name, ['student_id', 'item_id'])

        # Adding model 'Score'
        db.create_table(u'fest_score', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scored_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fest.Student'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fest.Item'])),
            ('mark', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'fest', ['Score'])

        # Adding unique constraint on 'Score', fields ['scored_by', 'student', 'item']
        db.create_unique(u'fest_score', ['scored_by_id', 'student_id', 'item_id'])

        # Adding model 'Result'
        db.create_table(u'fest_result', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fest.Item'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fest.Student'])),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('special', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'fest', ['Result'])


    def backwards(self, orm):
        # Removing unique constraint on 'Score', fields ['scored_by', 'student', 'item']
        db.delete_unique(u'fest_score', ['scored_by_id', 'student_id', 'item_id'])

        # Deleting model 'Item'
        db.delete_table(u'fest_item')

        # Deleting model 'Student'
        db.delete_table(u'fest_student')

        # Removing M2M table for field items on 'Student'
        db.delete_table(db.shorten_name(u'fest_student_items'))

        # Deleting model 'Score'
        db.delete_table(u'fest_score')

        # Deleting model 'Result'
        db.delete_table(u'fest_result')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'fest.item': {
            'Meta': {'object_name': 'Item'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_result_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'fest.result': {
            'Meta': {'object_name': 'Result'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fest.Item']"}),
            'score': ('django.db.models.fields.IntegerField', [], {}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fest.Student']"})
        },
        u'fest.score': {
            'Meta': {'unique_together': "(('scored_by', 'student', 'item'),)", 'object_name': 'Score'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fest.Item']"}),
            'mark': ('django.db.models.fields.IntegerField', [], {}),
            'scored_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fest.Student']"})
        },
        u'fest.student': {
            'Meta': {'object_name': 'Student'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['fest.Item']", 'symmetrical': 'False'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'schoolcode': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'std': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['fest']