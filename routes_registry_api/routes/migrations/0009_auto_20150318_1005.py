# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0008_remove_aquaticroute_states'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingplace',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(null=True, blank=True, srid=4674),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shippingplace',
            name='polygon',
            field=django.contrib.gis.db.models.fields.PolygonField(null=True, blank=True, srid=4674),
            preserve_default=True,
        ),
    ]
