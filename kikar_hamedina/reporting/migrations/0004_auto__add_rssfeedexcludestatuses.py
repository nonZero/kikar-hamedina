# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RSSFeedExcludeStatuses'
        db.create_table(u'reporting_rssfeedexcludestatuses', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='excluded_statuses', to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.related.ForeignKey')(related_name='excluded_by_users', to=orm['facebook_feeds.Facebook_Status'])),
        ))
        db.send_create_signal(u'reporting', ['RSSFeedExcludeStatuses'])


    def backwards(self, orm):
        # Deleting model 'RSSFeedExcludeStatuses'
        db.delete_table(u'reporting_rssfeedexcludestatuses')


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
        u'facebook_feeds.facebook_feed': {
            'Meta': {'ordering': "['feed_type']", 'object_name': 'Facebook_Feed'},
            'about': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'current_fan_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'feed_type': ('django.db.models.fields.CharField', [], {'default': "'PP'", 'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_current': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'locally_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1970, 1, 1, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'persona': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'feeds'", 'to': u"orm['facebook_feeds.Facebook_Persona']"}),
            'picture_large': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'picture_square': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'requires_user_token': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'username': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'vendor_id': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'})
        },
        u'facebook_feeds.facebook_persona': {
            'Meta': {'object_name': 'Facebook_Persona'},
            'alt_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'alt'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'alt_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_feed': ('django.db.models.fields.SmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'facebook_feeds.facebook_status': {
            'Meta': {'object_name': 'Facebook_Status'},
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['facebook_feeds.Facebook_Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_comment': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'like_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'locally_updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(1970, 1, 1, 0, 0)', 'blank': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {}),
            'share_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'status_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'status_type': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'story': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'story_tags': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'reporting.rssfeedexcludestatuses': {
            'Meta': {'object_name': 'RSSFeedExcludeStatuses'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'excluded_by_users'", 'to': u"orm['facebook_feeds.Facebook_Status']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'excluded_statuses'", 'to': u"orm['auth.User']"})
        },
        u'reporting.rssfeedkeyword': {
            'Meta': {'object_name': 'RSSFeedKeyWord'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'words_in_rss_feed'", 'to': u"orm['auth.User']"})
        },
        u'reporting.weeklyreportrecipients': {
            'Meta': {'object_name': 'WeeklyReportRecipients'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_beta': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['reporting']