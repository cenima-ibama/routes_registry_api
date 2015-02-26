# -*- coding: utf-8 -*-
from django_filters import FilterSet, CharFilter

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import DjangoFilterBackend
from rest_framework_gis.filters import InBBoxFilter

from .serializers import StateSerializer, PortSerializer
from .serializers import AirportSerializer
from .serializers import RoadRouteSerializer
from .serializers import AquaticRouteSerializer, AerialRouteSerializer
from .models import State, Port, Airport
from .models import RoadRoute, AerialRoute, AquaticRoute


class StateDetail(RetrieveUpdateDestroyAPIView):
    '''Detail of each state as a geojson feature format'''
    model = State
    serializer_class = StateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'code'


class PortList(ListCreateAPIView):
    '''Create or list all ports in geojson format'''
    model = Port
    serializer_class = PortSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class AirportNameFilter(FilterSet):
    '''Filter airports by name'''
    name = CharFilter(name='name', lookup_type='icontains')

    class Meta:
        model = Airport
        fields = ['name']


class AirportList(ListCreateAPIView):
    '''Create or list airports in geojson format. It is possible to filter
    by name or passing a bbox coordinates'''
    model = Airport
    serializer_class = AirportSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    bbox_filter_field = 'geom'
    filter_backends = (InBBoxFilter, DjangoFilterBackend,)
    filter_class = AirportNameFilter


class RoadRouteList(ListCreateAPIView):
    '''Create RoadRoute or list in geojson format'''
    model = RoadRoute
    serializer_class = RoadRouteSerializer
    permission_classes = (IsAuthenticated,)


class RoadRouteDetail(RetrieveUpdateDestroyAPIView):
    '''Detail of RoadRoutes'''
    model = RoadRoute
    serializer_class = RoadRouteSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'auth_code'


class RoadRouteGeoJSONDetail(ListAPIView):
    '''Detail of RoadRoutes in GeoJSON FeatureCollection format'''
    model = RoadRoute
    serializer_class = RoadRouteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(RoadRouteGeoJSONDetail, self).get_queryset()
        return queryset.filter(pk=self.kwargs.get('pk'))


class AerialRouteList(ListCreateAPIView):
    '''Create or List AerialRoutes'''
    model = AerialRoute
    serializer_class = AerialRouteSerializer
    permission_classes = (IsAuthenticated,)


class AerialRouteDetail(RetrieveUpdateDestroyAPIView):
    '''Detail of an AerialRoute'''
    model = AerialRoute
    serializer_class = AerialRouteSerializer
    permission_classes = (IsAuthenticated,)


class AquaticRouteList(ListCreateAPIView):
    '''Create or list AquaticRoutes'''
    model = AquaticRoute
    serializer_class = AquaticRouteSerializer
    permission_classes = (IsAuthenticated,)


class AquaticRouteDetail(RetrieveUpdateDestroyAPIView):
    '''Detail of an AquaticRoute'''
    model = AquaticRoute
    serializer_class = AquaticRouteSerializer
    permission_classes = (IsAuthenticated,)
