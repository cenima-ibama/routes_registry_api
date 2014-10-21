# -*- coding: utf-8 -*-
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.serializers import ModelSerializer

from .models import State, Company, RoadRoute


class CompanySerializer(ModelSerializer):

    class Meta:
        model = Company
        fields = ('id', 'name', 'states')


class StateSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = State
        geo_field = 'geom'
        fields = ('code', 'name')


class RoadRouteSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = RoadRoute
        geo_field = 'geom'
        fields = ('id', 'company')