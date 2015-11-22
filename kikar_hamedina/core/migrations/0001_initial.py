# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSearch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('queryset', models.TextField(default=b'eyJjb25uZWN0b3IiOiAiQU5EIiwgIm5lZ2F0ZWQiOiBmYWxzZSwgImNoaWxkcmVuIjogW119')),
                ('path', models.TextField(default=b'')),
                ('title', models.SlugField(unique=True, max_length=64)),
                ('description', models.TextField(null=True)),
                ('date_range', models.TextField(null=True)),
                ('order_by', models.TextField(null=True)),
                ('user', models.ForeignKey(related_name='queries', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
