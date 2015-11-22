# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('persons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordinal', models.IntegerField(verbose_name='Ordinal')),
                ('votes', models.IntegerField(help_text='How many people voted for this person', null=True, verbose_name='Elected by #', blank=True)),
                ('is_current', models.BooleanField(default=True, db_index=True)),
            ],
            options={
                'ordering': ('ordinal',),
            },
        ),
        migrations.CreateModel(
            name='CandidateList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, verbose_name='\u05e9\u05dd')),
                ('ballot', models.CharField(max_length=4, verbose_name='Ballot')),
                ('number_of_seats', models.IntegerField(null=True, blank=True)),
                ('mpg_html_report', models.TextField(help_text='The MPG report on the list, can use html', null=True, verbose_name='MPG report', blank=True)),
                ('img_url', models.URLField(blank=True)),
                ('youtube_user', models.CharField(max_length=80, null=True, verbose_name='YouTube user', blank=True)),
                ('wikipedia_page', models.CharField(max_length=512, null=True, verbose_name='Wikipedia page', blank=True)),
                ('twitter_account', models.CharField(max_length=80, null=True, verbose_name='Twitter account', blank=True)),
                ('facebook_url', models.URLField(null=True, blank=True)),
                ('platform', models.TextField(null=True, verbose_name='Platform', blank=True)),
                ('candidates', models.ManyToManyField(to='persons.Person', through='polyorg.Candidate', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CandidateListAltname',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('member', models.ForeignKey(to='polyorg.CandidateList')),
            ],
        ),
        migrations.CreateModel(
            name='ElectedKnesset',
            fields=[
                ('number', models.IntegerField(serialize=False, verbose_name='Elected Knesset number', primary_key=True)),
                ('start_date', models.DateField(null=True, verbose_name='Start date', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name='End date', blank=True)),
                ('election_date', models.DateField(null=True, verbose_name='Election date', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('accepts_memberships', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name_plural': 'parties',
            },
        ),
        migrations.AddField(
            model_name='candidatelist',
            name='knesset',
            field=models.ForeignKey(related_name='candidate_lists', blank=True, to='polyorg.ElectedKnesset', null=True),
        ),
        migrations.AddField(
            model_name='candidatelist',
            name='party',
            field=models.ForeignKey(blank=True, to='polyorg.Party', null=True),
        ),
        migrations.AddField(
            model_name='candidatelist',
            name='surplus_partner',
            field=models.ForeignKey(blank=True, to='polyorg.CandidateList', help_text='The list with which is the surplus votes partner', null=True),
        ),
        migrations.AddField(
            model_name='candidate',
            name='candidates_list',
            field=models.ForeignKey(to='polyorg.CandidateList'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='person',
            field=models.ForeignKey(to='persons.Person'),
        ),
    ]
