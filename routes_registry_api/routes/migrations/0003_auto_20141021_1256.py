# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0002_auto_20140924_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoadRoute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geom', django.contrib.gis.db.models.fields.LineStringField(srid=4674)),
                ('company', models.ForeignKey(to='routes.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='route',
            name='company',
        ),
        migrations.DeleteModel(
            name='Route',
        ),
    ]
