# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0005_roadroute_roads'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aerialroute',
            name='states',
        ),
    ]
