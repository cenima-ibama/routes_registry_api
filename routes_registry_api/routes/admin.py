from django.contrib.gis import admin
from .models import Company, State, Port, Airport
from .models import RoadRoute, AerialRoute, AquaticRoute


admin.site.register(Company, admin.OSMGeoAdmin)
admin.site.register(State, admin.OSMGeoAdmin)
admin.site.register(Port, admin.OSMGeoAdmin)
admin.site.register(Airport, admin.OSMGeoAdmin)
admin.site.register(RoadRoute, admin.OSMGeoAdmin)
admin.site.register(AerialRoute, admin.OSMGeoAdmin)
admin.site.register(AquaticRoute, admin.OSMGeoAdmin)