# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Jourie'
        db.delete_table(u'fest_jourie')

        # Removing M2M table for field items on 'Jourie'
        db.delete_table(db.shorten_name(u'fest_jourie_items'))

        # Adding model 'Jury'
        db.create_table(u'fest_jury', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('bio', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'fest', ['Jury'])

        # Adding M2M table for field items on 'Jury'
        m2m_table_name = db.shorten_name(u'fest_jury_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('jury', models.ForeignKey(orm[u'fest.jury'], null=False)),
            ('item', models.ForeignKey(orm[u'fest.item'], null=False))
        ))
        db.create_unique(m2m_table_name, ['jury_id', 'item_id'])


    def backwards(self, orm):
        # Adding model 'Jourie'
        db.create_table(u'fest_jourie', (
            ('bio', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'fest', ['Jourie'])

        # Adding M2M table for field items on 'Jourie'
        m2m_table_name = db.shorten_name(u'fest_jourie_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('jourie', models.ForeignKey(orm[u'fest.jourie'], null=False)),
            ('item', models.ForeignKey(orm[u'fest.item'], null=False))
        ))
        db.create_unique(m2m_table_name, ['jourie_id', 'item_id'])

        # Deleting model 'Jury'
        db.delete_table(u'fest_jury')

        # Removing M2M table for field items on 'Jury'
        db.delete_table(db.shorten_name(u'fest_jury_items'))


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
            'category': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_result_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'fest.jury': {
            'Meta': {'object_name': 'Jury'},
            'bio': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['fest.Item']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'fest.result': {
            'Meta': {'object_name': 'Result'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fest.Item']"}),
            'score': ('django.db.models.fields.IntegerField', [], {}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fest.Student']"}),
            'student_score': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'fest.score': {
            'Meta': {'unique_together': "(('scored_by', 'student', 'item'),)", 'object_name': 'Score'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_student': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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