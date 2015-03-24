# -*- coding: utf-8 -*-
from django_filters import FilterSet, CharFilter

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import DjangoFilterBackend
from rest_framework_gis.filters import InBBoxFilter

from .serializers import StateSerializer
from .serializers import ShippingPlaceSerializer, FloatsSerializer
from .serializers import AirportSerializer
from .serializers import RoadRouteSerializer
from .serializers import AerialRouteSerializer
from .serializers import SeaRouteSerializer
from .serializers import RiverRouteSerializer
from .models import State, ShippingPlace, Airport
from .models import RoadRoute, AerialRoute, SeaRoute, RiverRoute


class StateDetail(RetrieveUpdateDestroyAPIView):
    '''Detail of each state as a geojson feature format'''
    model = State
    serializer_class = StateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    lookup_field = 'code'


class ShippingPlaceList(ListCreateAPIView):
    '''List ShippingPlaces in geojson format'''
    model = ShippingPlace
    serializer_class = ShippingPlaceSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CreateFloatsView(ListCreateAPIView):
    '''View to create floats and minifloats ShippinPlace objects'''
    model = ShippingPlace
    serializer_class = FloatsSerializer
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
    lookup_field = 'auth_code'


class SeaRouteList(ListCreateAPIView):
    '''Create or list SeaRoutes'''
    model = SeaRoute
    serializer_class = SeaRouteSerializer
    permission_classes = (IsAuthenticated,)


class SeaRouteDetail(RetrieveUpdateDestroyAPIView):
    '''Detail of an SeaRoute'''
    model = SeaRoute
    serializer_class = SeaRouteSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'auth_code'


class RiverRouteList(ListCreateAPIView):
    '''Create or list RiverRoutes'''
    model = RiverRoute
    serializer_class = RiverRouteSerializer
    permission_classes = (IsAuthenticated,)


class RiverRouteDetail(RetrieveUpdateDestroyAPIView):
    '''Detail of an RiverRoute'''
    model = SeaRoute
    serializer_class = RiverRouteSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'auth_code'
