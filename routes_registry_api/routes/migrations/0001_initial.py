# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AerialRoute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.IntegerField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Aerial Route',
                'verbose_name_plural': 'Aerial Routes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4674)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AquaticRoute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.IntegerField()),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Aquatic Route',
                'verbose_name_plural': 'Aquatic Routes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4674)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoadRoute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.IntegerField()),
                ('geom', django.contrib.gis.db.models.fields.LineStringField(srid=4674)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Road Route',
                'verbose_name_plural': 'Road Routes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('code', models.CharField(max_length=2)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4674)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='roadroute',
            name='states',
            field=models.ManyToManyField(to='routes.State'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aquaticroute',
            name='destination',
            field=models.ForeignKey(related_name='route_destination', to='routes.Port'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aquaticroute',
            name='origin',
            field=models.ForeignKey(related_name='route_origin', to='routes.Port'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aquaticroute',
            name='states',
            field=models.ManyToManyField(to='routes.State'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aerialroute',
            name='destination',
            field=models.ForeignKey(related_name='route_destination', to='routes.Airport'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aerialroute',
            name='origin',
            field=models.ForeignKey(related_name='route_origin', to='routes.Airport'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='aerialroute',
            name='states',
            field=models.ManyToManyField(to='routes.State'),
            preserve_default=True,
        ),
    ]
