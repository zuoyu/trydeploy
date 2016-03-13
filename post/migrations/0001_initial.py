# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('guid', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('remote_author_name', models.CharField(default=b'', max_length=100, blank=True)),
                ('remote_author_url', models.CharField(default=b'', max_length=1000, blank=True)),
                ('content', models.CharField(max_length=1000)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('local_author', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_type', models.CharField(max_length=50, choices=[(b'jpeg', b'JPG/JPEG'), (b'png', b'PNG'), (b'gif', b'GIF'), (b'bmp', b'BMP')])),
                ('image_data', models.BinaryField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, serialize=False, editable=False, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('description', models.CharField(max_length=1000)),
                ('content', models.CharField(max_length=5000)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now_add=True)),
                ('privacy_level', models.CharField(default=b'pub', max_length=10, blank=True, choices=[(b'pub', b'Public'), (b'me', b'Private to me'), (b'friends', b'Friends only'), (b'fof', b'Friends of friends')])),
                ('privacy_host_only', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('privacy_whitelist', models.ManyToManyField(related_name='+', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='image',
            name='parent_post',
            field=models.ForeignKey(to='post.Post'),
        ),
        migrations.AddField(
            model_name='image',
            name='uploader',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(to='post.Post'),
        ),
    ]
