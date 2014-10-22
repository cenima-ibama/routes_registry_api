# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0005_auto_20141022_0436'),
    ]

    operations = [
        migrations.CreateModel(
            name='AquaticRoute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('origin', django.contrib.gis.db.models.fields.PointField(srid=4674)),
                ('destination', django.contrib.gis.db.models.fields.PointField(srid=4674)),
                ('company', models.ForeignKey(to='routes.Company')),
            ],
            options={
                'verbose_name': 'Aquatic Route',
                'verbose_name_plural': 'Aquatic Routes',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='airroute',
            name='company',
        ),
        migrations.DeleteModel(
            name='AirRoute',
        ),
    ]
