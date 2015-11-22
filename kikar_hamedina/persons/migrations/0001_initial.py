# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('img_url', models.URLField(null=True, blank=True)),
                ('phone', models.CharField(max_length=20, null=True, blank=True)),
                ('fax', models.CharField(max_length=20, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('family_status', models.CharField(max_length=10, null=True, blank=True)),
                ('number_of_children', models.IntegerField(null=True, blank=True)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('place_of_birth', models.CharField(max_length=100, null=True, blank=True)),
                ('date_of_death', models.DateField(null=True, blank=True)),
                ('year_of_aliyah', models.IntegerField(null=True, blank=True)),
                ('place_of_residence', models.CharField(help_text='an accurate place of residence (for example, an address', max_length=100, null=True, blank=True)),
                ('area_of_residence', models.CharField(help_text='a general area of residence (for example, "the negev"', max_length=100, null=True, blank=True)),
                ('place_of_residence_lat', models.CharField(max_length=16, null=True, blank=True)),
                ('place_of_residence_lon', models.CharField(max_length=16, null=True, blank=True)),
                ('residence_centrality', models.IntegerField(null=True, blank=True)),
                ('residence_economy', models.IntegerField(null=True, blank=True)),
                ('gender', models.CharField(blank=True, max_length=1, null=True, choices=[('M', 'Male'), ('F', 'Female')])),
                ('mk', models.ForeignKey(related_name='person', blank=True, to='mks.Member', null=True)),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Person',
                'verbose_name_plural': 'Persons',
            },
        ),
        migrations.CreateModel(
            name='PersonAltname',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('person', models.ForeignKey(to='persons.Person')),
            ],
        ),
        migrations.CreateModel(
            name='ProcessedProtocolPart',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('protocol_part_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('text', models.CharField(max_length=1024, null=True, blank=True)),
                ('org', models.TextField(null=True, blank=True)),
                ('person', models.ForeignKey(related_name='roles', to='persons.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='titles',
            field=models.ManyToManyField(related_name='persons', to='persons.Title', blank=True),
        ),
    ]
