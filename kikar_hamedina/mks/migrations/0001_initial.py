# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('planet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoalitionMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
            ],
            options={
                'ordering': ('party', 'start_date'),
            },
        ),
        migrations.CreateModel(
            name='Correlation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=0)),
                ('normalized_score', models.FloatField(null=True)),
                ('not_same_party', models.NullBooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Knesset',
            fields=[
                ('number', models.IntegerField(serialize=False, verbose_name='Knesset number', primary_key=True)),
                ('start_date', models.DateField(null=True, verbose_name='Start date', blank=True)),
                ('end_date', models.DateField(null=True, verbose_name='End date', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('current_position', models.PositiveIntegerField(default=999, blank=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('img_url', models.URLField(blank=True)),
                ('phone', models.CharField(max_length=20, null=True, blank=True)),
                ('fax', models.CharField(max_length=20, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('website', models.URLField(null=True, blank=True)),
                ('family_status', models.CharField(max_length=10, null=True, blank=True)),
                ('number_of_children', models.IntegerField(null=True, blank=True)),
                ('date_of_birth', models.DateField(null=True, blank=True)),
                ('place_of_birth', models.CharField(max_length=100, null=True, blank=True)),
                ('date_of_death', models.DateField(null=True, blank=True)),
                ('year_of_aliyah', models.IntegerField(null=True, blank=True)),
                ('is_current', models.BooleanField(default=True, db_index=True)),
                ('place_of_residence', models.CharField(help_text='an accurate place of residence (for example, an address', max_length=100, null=True, blank=True)),
                ('area_of_residence', models.CharField(help_text='a general area of residence (for example, "the negev"', max_length=100, null=True, blank=True)),
                ('place_of_residence_lat', models.CharField(max_length=16, null=True, blank=True)),
                ('place_of_residence_lon', models.CharField(max_length=16, null=True, blank=True)),
                ('residence_centrality', models.IntegerField(null=True, blank=True)),
                ('residence_economy', models.IntegerField(null=True, blank=True)),
                ('gender', models.CharField(blank=True, max_length=1, null=True, choices=[('M', 'Male'), ('F', 'Female')])),
                ('current_role_descriptions', models.CharField(max_length=1024, null=True, blank=True)),
                ('bills_stats_proposed', models.IntegerField(default=0)),
                ('bills_stats_pre', models.IntegerField(default=0)),
                ('bills_stats_first', models.IntegerField(default=0)),
                ('bills_stats_approved', models.IntegerField(default=0)),
                ('average_weekly_presence_hours', models.FloatField(null=True, blank=True)),
                ('average_monthly_committee_presence', models.FloatField(null=True, blank=True)),
                ('backlinks_enabled', models.BooleanField(default=True)),
                ('blog', models.OneToOneField(null=True, blank=True, to='planet.Blog')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Member',
                'verbose_name_plural': 'Members',
            },
        ),
        migrations.CreateModel(
            name='MemberAltname',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('member', models.ForeignKey(to='mks.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('position', models.PositiveIntegerField(default=999, blank=True)),
                ('member', models.ForeignKey(to='mks.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('is_coalition', models.BooleanField(default=False)),
                ('number_of_members', models.IntegerField(null=True, blank=True)),
                ('number_of_seats', models.IntegerField(null=True, blank=True)),
                ('logo', models.ImageField(null=True, upload_to=b'partyLogos', blank=True)),
                ('knesset', models.ForeignKey(related_name='parties', blank=True, to='mks.Knesset', null=True)),
            ],
            options={
                'ordering': ('-number_of_seats',),
                'verbose_name': 'Party',
                'verbose_name_plural': 'Parties',
            },
        ),
        migrations.CreateModel(
            name='PartyAltname',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('member', models.ForeignKey(to='mks.Party')),
            ],
        ),
        migrations.CreateModel(
            name='WeeklyPresence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(null=True, blank=True)),
                ('hours', models.FloatField(blank=True)),
                ('member', models.ForeignKey(to='mks.Member')),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='party',
            field=models.ForeignKey(to='mks.Party'),
        ),
        migrations.AddField(
            model_name='member',
            name='current_party',
            field=models.ForeignKey(related_name='members', blank=True, to='mks.Party', null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='parties',
            field=models.ManyToManyField(related_name='all_members', through='mks.Membership', to='mks.Party'),
        ),
        migrations.AddField(
            model_name='member',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='correlation',
            name='m1',
            field=models.ForeignKey(related_name='m1', to='mks.Member'),
        ),
        migrations.AddField(
            model_name='correlation',
            name='m2',
            field=models.ForeignKey(related_name='m2', to='mks.Member'),
        ),
        migrations.AddField(
            model_name='coalitionmembership',
            name='party',
            field=models.ForeignKey(related_name='coalition_memberships', to='mks.Party'),
        ),
        migrations.AlterUniqueTogether(
            name='party',
            unique_together=set([('knesset', 'name')]),
        ),
    ]
