# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0007_auto_20150317_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aquaticroute',
            name='states',
        ),
    ]
