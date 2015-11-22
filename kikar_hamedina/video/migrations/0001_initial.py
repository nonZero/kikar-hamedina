# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=2000, blank=True)),
                ('embed_link', models.URLField(max_length=1000)),
                ('image_link', models.URLField(max_length=1000)),
                ('small_image_link', models.URLField(max_length=1000)),
                ('link', models.URLField(max_length=1000)),
                ('source_type', models.CharField(max_length=50)),
                ('source_id', models.CharField(max_length=255)),
                ('group', models.CharField(max_length=20)),
                ('published', models.DateTimeField()),
                ('sticky', models.BooleanField(default=False)),
                ('hide', models.BooleanField(default=False)),
                ('object_pk', models.TextField()),
                ('reviewed', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
        ),
    ]
