# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0011_auto_20150402_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roadroute',
            name='roads',
            field=models.TextField(),
            preserve_default=True,
        ),
    ]
