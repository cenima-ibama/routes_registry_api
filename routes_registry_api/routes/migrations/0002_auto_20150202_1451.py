# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aerialroute',
            name='company',
        ),
        migrations.RemoveField(
            model_name='aquaticroute',
            name='company',
        ),
        migrations.RemoveField(
            model_name='roadroute',
            name='company',
        ),
        migrations.AddField(
            model_name='aerialroute',
            name='auth_code',
            field=models.CharField(max_length=40, unique=True, default='2015-02-02 16:51:06.262374+00:00', verbose_name='Authorization Code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aquaticroute',
            name='auth_code',
            field=models.CharField(max_length=40, unique=True, default='2015-02-02 16:51:17.134374+00:00', verbose_name='Authorization Code'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roadroute',
            name='auth_code',
            field=models.CharField(max_length=40, unique=True, default='2015-02-02 16:51:19.926371+00:00', verbose_name='Authorization Code'),
            preserve_default=False,
        ),
    ]
