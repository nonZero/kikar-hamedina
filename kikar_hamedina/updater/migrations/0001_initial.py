# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseExecutor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LikesRule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_time_analysed', models.DateTimeField()),
                ('min_likes', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EmailUpdater',
            fields=[
                ('baseexecutor_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='updater.BaseExecutor')),
                ('subscribers', jsonfield.fields.JSONField(default=[])),
            ],
            options={
                'abstract': False,
            },
            bases=('updater.baseexecutor',),
        ),
        migrations.AddField(
            model_name='likesrule',
            name='executors',
            field=models.ManyToManyField(to='updater.BaseExecutor'),
        ),
        migrations.AddField(
            model_name='likesrule',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_updater.likesrule_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
        migrations.AddField(
            model_name='baseexecutor',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_updater.baseexecutor_set+', editable=False, to='contenttypes.ContentType', null=True),
        ),
    ]
