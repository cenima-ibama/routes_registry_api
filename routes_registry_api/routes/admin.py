from django.contrib.gis import admin
from .models import Company, State, Route


admin.site.register(Company, admin.OSMGeoAdmin)
admin.site.register(State, admin.OSMGeoAdmin)
admin.site.register(Route, admin.OSMGeoAdmin)