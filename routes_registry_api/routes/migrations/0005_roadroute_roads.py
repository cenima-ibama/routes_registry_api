# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0004_auto_20150313_1751'),
    ]

    operations = [
        migrations.AddField(
            model_name='roadroute',
            name='roads',
            field=models.CharField(default='BA-001', max_length=255),
            preserve_default=False,
        ),
    ]
