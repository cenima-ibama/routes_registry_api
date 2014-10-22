from django.contrib.gis import admin
from .models import Company, State, RoadRoute, AirRoute


admin.site.register(Company, admin.OSMGeoAdmin)
admin.site.register(State, admin.OSMGeoAdmin)
admin.site.register(RoadRoute, admin.OSMGeoAdmin)
admin.site.register(AirRoute, admin.OSMGeoAdmin)