# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0003_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='roadroute',
            name='destination',
            field=models.ForeignKey(blank=True, to='routes.City', related_name='roadroute_destination', default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roadroute',
            name='origin',
            field=models.ForeignKey(blank=True, to='routes.City', related_name='roadroute_origin', default=1),
            preserve_default=False,
        ),
    ]
