# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0006_remove_aerialroute_states'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShippingPlace',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=50, choices=[('seaport', 'Seaport'), ('river_port', 'River port'), ('float', 'Float'), ('mini_float', 'Mini float'), ('sea_basin', 'Sea basin'), ('river_basin', 'River basin')])),
                ('point', django.contrib.gis.db.models.fields.PointField(srid=4674, null=True)),
                ('polygon', django.contrib.gis.db.models.fields.PolygonField(srid=4674, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='aquaticroute',
            name='destination',
            field=models.ForeignKey(related_name='route_destination', to='routes.ShippingPlace'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='aquaticroute',
            name='origin',
            field=models.ForeignKey(related_name='route_origin', to='routes.ShippingPlace'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='Port',
        ),
    ]
