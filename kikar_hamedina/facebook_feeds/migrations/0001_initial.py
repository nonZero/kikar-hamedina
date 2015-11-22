# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
import facebook_feeds.models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Facebook_Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vendor_id', models.TextField(null=True, blank=True)),
                ('username', models.TextField(default=None, null=True, blank=True)),
                ('birthday', models.TextField(null=True, blank=True)),
                ('name', models.TextField(null=True, blank=True)),
                ('link', models.URLField(max_length=2000, null=True, blank=True)),
                ('picture_square', models.URLField(max_length=2000, null=True, blank=True)),
                ('picture_large', models.URLField(max_length=2000, null=True, blank=True)),
                ('feed_type', models.CharField(default=b'PP', max_length=2, choices=[(b'PP', b'Public Page'), (b'UP', b'User Profile'), (b'NA', b'Unavailable Profile'), (b'DP', b'Deprecated Profile')])),
                ('requires_user_token', models.BooleanField(default=False)),
                ('is_current', models.BooleanField(default=True)),
                ('current_fan_count', models.IntegerField(default=0)),
                ('locally_updated', models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0), null=True, blank=True)),
                ('about', models.TextField(default=b'', null=True, blank=True)),
                ('website', models.URLField(max_length=2000, null=True, blank=True)),
            ],
            options={
                'ordering': ['feed_type'],
            },
        ),
        migrations.CreateModel(
            name='Facebook_Persona',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('alt_object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('main_feed', models.SmallIntegerField(default=0, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Facebook_Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status_id', models.CharField(unique=True, max_length=128)),
                ('content', models.TextField()),
                ('like_count', models.PositiveIntegerField(default=0, blank=True)),
                ('comment_count', models.PositiveIntegerField(default=0, blank=True)),
                ('share_count', models.PositiveIntegerField(default=0, blank=True)),
                ('published', models.DateTimeField()),
                ('updated', models.DateTimeField()),
                ('status_type', models.CharField(default=None, max_length=128, null=True, blank=True)),
                ('story', models.TextField(null=True, blank=True)),
                ('story_tags', models.TextField(null=True, blank=True)),
                ('is_comment', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('locally_updated', models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0), blank=True)),
                ('feed', models.ForeignKey(to='facebook_feeds.Facebook_Feed')),
            ],
            options={
                'verbose_name_plural': 'Facebook_Statuses',
            },
        ),
        migrations.CreateModel(
            name='Facebook_Status_Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(null=True, blank=True)),
                ('caption', models.TextField(null=True, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('link', models.TextField()),
                ('facebook_object_id', models.CharField(max_length=128, null=True, blank=True)),
                ('type', models.CharField(blank=True, max_length=16, null=True, choices=[(b'status', b'Status'), (b'video', b'Video'), (b'photo', b'Photo'), (b'link', b'Link')])),
                ('picture', models.TextField(null=True, blank=True)),
                ('source', models.TextField(null=True, blank=True)),
                ('source_width', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('source_height', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('status', models.OneToOneField(related_name='attachment', to='facebook_feeds.Facebook_Status')),
            ],
        ),
        migrations.CreateModel(
            name='Feed_Popularity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_of_creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('talking_about_count', models.IntegerField(default=0)),
                ('fan_count', models.IntegerField(default=0)),
                ('followers_count', models.IntegerField(default=0)),
                ('friends_count', models.IntegerField(default=0)),
                ('feed', models.ForeignKey(to='facebook_feeds.Facebook_Feed')),
            ],
            options={
                'ordering': ['-date_of_creation'],
                'verbose_name_plural': 'Feed_Popularities',
            },
        ),
        migrations.CreateModel(
            name='Status_Comment_Pattern',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pattern', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('is_for_main_display', models.BooleanField(default=True)),
                ('statuses', models.ManyToManyField(related_name='old_tags', to='facebook_feeds.Facebook_Status')),
            ],
        ),
        migrations.CreateModel(
            name='User_Token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(unique=True, max_length=256)),
                ('user_id', models.TextField(unique=True)),
                ('date_of_creation', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_of_expiration', models.DateTimeField(default=facebook_feeds.models.later)),
                ('feeds', models.ManyToManyField(related_name='tokens', to='facebook_feeds.Facebook_Feed')),
            ],
        ),
    ]
