# -*- coding: utf-8 -*-
from django_filters import FilterSet

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

    class Meta:
        model = Airport
        fields = ['name']


class AirportList(ListCreateAPIView):
    '''Create or list airports in geojson format'''
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


class AerialRouteOrigin(ListAPIView):
    '''Return a GeoJSON with the origin airport of the route.'''
    model = Airport
    serializer_class = AirportSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(AerialRouteOrigin, self).get_queryset()
        return queryset.filter(route_origin__pk=self.kwargs.get('pk'))


class AerialRouteDestination(ListAPIView):
    '''Return a GeoJSON with the destination airport of the route.'''
    model = Airport
    serializer_class = AirportSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(AerialRouteDestination, self).get_queryset()
        return queryset.filter(route_destination__pk=self.kwargs.get('pk'))


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


class AquaticRouteOrigin(ListAPIView):
    '''Return a GeoJSON with the origin port of the route.'''
    model = Port
    serializer_class = AirportSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(AquaticRouteOrigin, self).get_queryset()
        return queryset.filter(route_origin__pk=self.kwargs.get('pk'))


class AquaticRouteDestination(ListAPIView):
    '''Return a GeoJSON with the destination port of the route.'''
    model = Port
    serializer_class = AirportSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(AquaticRouteDestination, self).get_queryset()
        return queryset.filter(route_destination__pk=self.kwargs.get('pk'))