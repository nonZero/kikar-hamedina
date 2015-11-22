# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('kikartags', '0001_initial'),
        ('facebook_feeds', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebook_status',
            name='tags',
            field=taggit.managers.TaggableManager(to='kikartags.Tag', through='kikartags.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags'),
        ),
        migrations.AddField(
            model_name='facebook_persona',
            name='alt_content_type',
            field=models.ForeignKey(related_name='alt', blank=True, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='facebook_persona',
            name='content_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='facebook_feed',
            name='persona',
            field=models.ForeignKey(related_name='feeds', to='facebook_feeds.Facebook_Persona'),
        ),
    ]
