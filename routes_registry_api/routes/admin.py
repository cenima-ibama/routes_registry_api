from django.contrib.gis import admin
from .models import State, City, ShippingPlace, Airport
from .models import RoadRoute, AerialRoute, SeaRoute, RiverRoute


admin.site.register(State, admin.OSMGeoAdmin)
admin.site.register(City, admin.OSMGeoAdmin)
admin.site.register(ShippingPlace, admin.OSMGeoAdmin)
admin.site.register(Airport, admin.OSMGeoAdmin)
admin.site.register(RoadRoute, admin.OSMGeoAdmin)
admin.site.register(AerialRoute, admin.OSMGeoAdmin)
admin.site.register(SeaRoute, admin.OSMGeoAdmin)
admin.site.register(RiverRoute, admin.OSMGeoAdmin)