# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0004_auto_20141022_0420'),
    ]

    operations = [
        migrations.CreateModel(
            name='AerialRoute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('origin', django.contrib.gis.db.models.fields.PointField(srid=4674)),
                ('destination', django.contrib.gis.db.models.fields.PointField(srid=4674)),
                ('company', models.ForeignKey(to='routes.Company')),
            ],
            options={
                'verbose_name': 'Aerial Route',
                'verbose_name_plural': 'Aerial Routes',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='airroute',
            options={'verbose_name': 'Air Route', 'verbose_name_plural': 'Air Routes'},
        ),
    ]
