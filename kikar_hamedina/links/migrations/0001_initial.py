# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.files.storage


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(max_length=1000, verbose_name=b'URL')),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('object_pk', models.TextField(verbose_name='object ID')),
                ('active', models.BooleanField(default=True)),
                ('content_type', models.ForeignKey(related_name='content_type_set_for_link', verbose_name='content type', to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name': 'link',
                'verbose_name_plural': 'links',
            },
        ),
        migrations.CreateModel(
            name='LinkedFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sha1', models.CharField(max_length=1000, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('link_file', models.FileField(storage=django.core.files.storage.FileSystemStorage(b'/home/udi/projects/kikar-hamedina/kikar_hamedina/data/link_files_storage'), upload_to=b'link_files')),
                ('link', models.ForeignKey(default=None, blank=True, to='links.Link', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LinkType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name='title')),
                ('image', models.ImageField(upload_to=b'icons')),
            ],
            options={
                'verbose_name': 'link type',
                'verbose_name_plural': 'link types',
            },
        ),
        migrations.AddField(
            model_name='link',
            name='link_type',
            field=models.ForeignKey(default=b'', blank=True, to='links.LinkType', null=True),
        ),
    ]
