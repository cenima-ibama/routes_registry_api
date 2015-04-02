# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0010_auto_20150323_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roadroute',
            name='destination',
            field=models.ForeignKey(blank=True, null=True, to='routes.City', related_name='roadroute_destination'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='roadroute',
            name='origin',
            field=models.ForeignKey(blank=True, null=True, to='routes.City', related_name='roadroute_origin'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='shippingplace',
            name='category',
            field=models.CharField(choices=[('seaport', 'Seaport'), ('riverport', 'River port'), ('float', 'Float'), ('minifloat', 'Mini float'), ('seabasin', 'Sea basin'), ('riverbasin', 'River basin')], max_length=50),
            preserve_default=True,
        ),
    ]
