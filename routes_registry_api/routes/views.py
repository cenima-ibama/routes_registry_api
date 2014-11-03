# -*- coding: utf-8 -*-
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .serializers import CompanySerializer, StateSerializer, PortSerializer
from .serializers import AirportSerializer, RoadRouteSerializer
from .serializers import AquaticRouteSerializer, AerialRouteSerializer
from .models import State, Company, Port, Airport
from .models import RoadRoute, AerialRoute, AquaticRoute


class StateDetail(RetrieveUpdateDestroyAPIView):
    '''Detail of each state as a geojson feature format'''
    model = State
    serializer_class = StateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CompanyList(ListCreateAPIView):
    '''Create or list companies'''
    model = Company
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CompanyDetail(RetrieveUpdateDestroyAPIView):
    '''Detail of each company'''
    model = Company
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CompanyAerialRoutes(ListAPIView):
    '''List all aerial routes of a company'''
    model = AerialRoute
    serializer_class = AerialRouteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(CompanyAerialRoutes, self).get_queryset()
        return queryset.filter(company__pk=self.kwargs.get('pk'))


class CompanyAquaticRoutes(ListAPIView):
    '''List all aquatic routes of a company'''
    model = AquaticRoute
    serializer_class = AquaticRouteSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super(CompanyAquaticRoutes, self).get_queryset()
        return queryset.filter(company__pk=self.kwargs.get('pk'))


class PortList(ListCreateAPIView):
    '''Create or list all ports in geojson format'''
    model = Port
    serializer_class = PortSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class AirportList(ListCreateAPIView):
    '''Create or list airports in geojson format'''
    model = Airport
    serializer_class = AirportSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


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
