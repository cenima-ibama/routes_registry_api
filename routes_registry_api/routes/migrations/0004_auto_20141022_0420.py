# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0003_auto_20141021_1256'),
    ]

    operations = [
        migrations.CreateModel(
            name='AirRoute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('origin', django.contrib.gis.db.models.fields.PointField(srid=4674)),
                ('destination', django.contrib.gis.db.models.fields.PointField(srid=4674)),
                ('company', models.ForeignKey(to='routes.Company')),
            ],
            options={
                'verbose_name': 'Road Route',
                'verbose_name_plural': 'Road Routes',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Company', 'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterModelOptions(
            name='roadroute',
            options={'verbose_name': 'Road Route', 'verbose_name_plural': 'Road Routes'},
        ),
    ]
