# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='aerialroute',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 27, 13, 23, 47, 19734, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aquaticroute',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 27, 13, 23, 50, 827713, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roadroute',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime(2014, 10, 27, 13, 23, 55, 179683, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
