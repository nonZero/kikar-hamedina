# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Slug')),
                ('is_for_main_display', models.BooleanField(default=True)),
                ('logo', models.ImageField(null=True, upload_to=b'tags_logos', blank=True)),
                ('is_suggestion', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
            },
        ),
        migrations.CreateModel(
            name='TaggedItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.IntegerField(verbose_name='Object id', db_index=True)),
                ('date_of_tagging', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('content_type', models.ForeignKey(related_name='kikartags_taggeditem_tagged_items', verbose_name='Content type', to='contenttypes.ContentType')),
                ('tag', models.ForeignKey(related_name='kikartags_taggeditem_items', to='kikartags.Tag')),
                ('tagged_by', models.ForeignKey(related_name='tagged', default=None, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TagSynonym',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('proper_form_of_tag', models.ForeignKey(related_name='synonyms', to='kikartags.Tag')),
                ('tag', models.ForeignKey(related_name='proper_form_of_tag', to='kikartags.Tag', unique=True)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='tagsynonym',
            unique_together=set([('tag', 'proper_form_of_tag')]),
        ),
    ]
