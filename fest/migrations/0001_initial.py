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
            ('category', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('is_result_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
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

        # Adding model 'Participant'
        db.create_table(u'fest_participant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fest.Item'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fest.Student'])),
            ('code', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'fest', ['Participant'])

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

        # Adding model 'Score'
        db.create_table(u'fest_score', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fest.Participant'])),
            ('scored_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('mark', self.gf('django.db.models.fields.IntegerField')()),
            ('is_student', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'fest', ['Score'])

        # Adding unique constraint on 'Score', fields ['scored_by', 'participant']
        db.create_unique(u'fest_score', ['scored_by_id', 'participant_id'])

        # Adding model 'Result'
        db.create_table(u'fest_result', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fest.Participant'])),
            ('score', self.gf('django.db.models.fields.FloatField')()),
            ('student_score', self.gf('django.db.models.fields.FloatField')(default=0)),
        ))
        db.send_create_signal(u'fest', ['Result'])

        # Adding model 'SpecialAward'
        db.create_table(u'fest_specialaward', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('participant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['fest.Participant'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'fest', ['SpecialAward'])


    def backwards(self, orm):
        # Removing unique constraint on 'Score', fields ['scored_by', 'participant']
        db.delete_unique(u'fest_score', ['scored_by_id', 'participant_id'])

        # Deleting model 'Item'
        db.delete_table(u'fest_item')

        # Deleting model 'Student'
        db.delete_table(u'fest_student')

        # Deleting model 'Participant'
        db.delete_table(u'fest_participant')

        # Deleting model 'Jury'
        db.delete_table(u'fest_jury')

        # Removing M2M table for field items on 'Jury'
        db.delete_table(db.shorten_name(u'fest_jury_items'))

        # Deleting model 'Score'
        db.delete_table(u'fest_score')

        # Deleting model 'Result'
        db.delete_table(u'fest_result')

        # Deleting model 'SpecialAward'
        db.delete_table(u'fest_specialaward')


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
        u'fest.participant': {
            'Meta': {'object_name': 'Participant'},
            'code': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fest.Item']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fest.Student']"})
        },
        u'fest.result': {
            'Meta': {'object_name': 'Result'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fest.Participant']"}),
            'score': ('django.db.models.fields.FloatField', [], {}),
            'student_score': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'fest.score': {
            'Meta': {'unique_together': "(('scored_by', 'participant'),)", 'object_name': 'Score'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_student': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mark': ('django.db.models.fields.IntegerField', [], {}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fest.Participant']"}),
            'scored_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'fest.specialaward': {
            'Meta': {'object_name': 'SpecialAward'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'participant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['fest.Participant']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'fest.student': {
            'Meta': {'object_name': 'Student'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'schoolcode': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'std': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['fest']