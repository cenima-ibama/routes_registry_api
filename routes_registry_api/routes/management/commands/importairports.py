# -*- coding: utf-8 -*-

import simplejson

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point

from ...models import Airport


class Command(BaseCommand):
    args = 'filename'
    help = 'Import airports from a GeoJSON file'

    def handle(self, *args, **options):
        for filename in args:
            data_json = open(filename, 'r').read()
            data = simplejson.loads(data_json)
            count = 0

            for feature in data['features']:
                if feature['properties'].get('name') is not None:
                    obj, created = Airport.objects.get_or_create(
                        name=feature['properties'].get('name'),
                        geom=Point(feature['geometry'].get('coordinates'))
                        )
                    if created:
                        count += 1

            print(('Imported %s airports' % count))