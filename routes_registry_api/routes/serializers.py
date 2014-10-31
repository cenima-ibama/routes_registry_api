# -*- coding: utf-8 -*-
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.serializers import ModelSerializer, Field

from .models import State, Company, Port, Airport
from .models import RoadRoute, AerialRoute, AquaticRoute


class CompanySerializer(ModelSerializer):

    class Meta:
        model = Company
        fields = ('id', 'name', 'states')


class StateSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = State
        geo_field = 'geom'
        fields = ('id', 'code', 'name')


class PortSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Port
        geo_field = 'geom'
        fields = ('id', 'name')


class AirportSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = Airport
        geo_field = 'geom'
        fields = ('id', 'name')


class RoadRouteSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = RoadRoute
        geo_field = 'geom'
        fields = ('id', 'company')


class AerialRouteSerializer(ModelSerializer):
    route = Field(source='route')

    class Meta:
        model = AerialRoute
        fields = ('id', 'company', 'origin', 'destination', 'route')


class AquaticRouteSerializer(ModelSerializer):
    route = Field(source='route')

    class Meta:
        model = AquaticRoute
        fields = ('id', 'company', 'origin', 'destination', 'route')