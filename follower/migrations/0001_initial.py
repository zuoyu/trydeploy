# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Follows',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('followed', models.ForeignKey(related_name='followed', to=settings.AUTH_USER_MODEL)),
                ('follower', models.ForeignKey(related_name='follower', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Following',
                'verbose_name_plural': 'Followers',
            },
        ),
        migrations.AlterUniqueTogether(
            name='follows',
            unique_together=set([('followed', 'follower')]),
        ),
    ]
