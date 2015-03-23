# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0009_auto_20150318_1005'),
    ]

    operations = [
        migrations.CreateModel(
            name='RiverRoute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth_code', models.CharField(verbose_name='Authorization Code', max_length=40, unique=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('destination', models.ForeignKey(to='routes.ShippingPlace', related_name='river_route_destination')),
                ('origin', models.ForeignKey(to='routes.ShippingPlace', related_name='river_route_origin')),
            ],
            options={
                'verbose_name': 'River Route',
                'verbose_name_plural': 'River Routes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SeaRoute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth_code', models.CharField(verbose_name='Authorization Code', max_length=40, unique=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('destination', models.ForeignKey(to='routes.ShippingPlace', related_name='searoute_destination')),
                ('origin', models.ForeignKey(to='routes.ShippingPlace', related_name='searoute_origin')),
            ],
            options={
                'verbose_name': 'Sea Route',
                'verbose_name_plural': 'Sea Routes',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='aquaticroute',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='aquaticroute',
            name='origin',
        ),
        migrations.DeleteModel(
            name='AquaticRoute',
        ),
    ]
