# -*- coding: utf-8 -*-
from django.utils.translation import ugettext, ugettext_lazy as _

from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis.fields import GeometryField
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.serializers import Field, SlugRelatedField

from .models import State, ShippingPlace, Airport
from .models import RoadRoute, AerialRoute, SeaRoute, RiverRoute


class StateSerializer(GeoFeatureModelSerializer):
    """Serializer to the State model."""

    class Meta:
        model = State
        geo_field = 'geom'
        fields = ('id', 'code', 'name')


class ShippingPlaceSerializer(GeoFeatureModelSerializer):
    """Serializer to the ShippingPlace model. Used only to serialize data."""

    geom = GeometryField(source='geom', read_only=True)

    class Meta:
        model = ShippingPlace
        geo_field = 'geom'
        fields = ('id', 'name', 'category')


class FloatsSerializer(GeoFeatureModelSerializer):
    """Serializer to the ShippingPlace model. Used only to deserialize data,
    allowing the users to create float and minifloat objects.
    """

    class Meta:
        model = ShippingPlace
        geo_field = 'point'
        fields = ('id', 'name', 'category')


class AirportSerializer(GeoFeatureModelSerializer):
    """Serializer to the Airport model."""

    class Meta:
        model = Airport
        geo_field = 'geom'
        fields = ('id', 'name')


class RoadRouteSerializer(GeoFeatureModelSerializer):
    """Serializer to the Road Route model. Only accept route creation if the
    states field is not empty and if the route is within the states geometry.
    """

    states = SlugRelatedField(many=True, read_only=False, slug_field='code')
    origin = Field(source='origin.__str__')
    destination = Field(source='destination.__str__')

    class Meta:
        model = RoadRoute
        id_field = False
        geo_field = 'geom'
        fields = ('auth_code', 'states', 'roads', 'origin', 'destination',
            'creation_date')

    def validate(self, attrs):
        if len(attrs['states']) > 0:
            states = State.objects.filter(code__in=attrs['states']).unionagg()
            if attrs['geom'].within(states) is False:
                raise ValidationError(_('Route is not within the allowed states.'))
            else:
                return attrs
        else:
            raise ValidationError(_('States field can not be empty.'))


class AerialRouteSerializer(GeoFeatureModelSerializer):
    """Serializer to the Aerial Route model. Furthermore the model fields, it
    includes the name of the origin and destination airports.
    """

    route = GeometryField(source='route', read_only=True)
    origin_name = Field(source='origin.name')
    destination_name = Field(source='destination.name')

    class Meta:
        model = AerialRoute
        id_field = False
        geo_field = 'route'
        fields = ('auth_code', 'origin', 'destination', 'origin_name',
            'destination_name', 'creation_date')


class SeaRouteSerializer(ModelSerializer):
    """Serializer to the SeaRoute model."""

    route = GeometryField(source='route', read_only=True)
    origin_name = Field(source='origin.name')
    destination_name = Field(source='destination.name')

    class Meta:
        model = SeaRoute
        id_field = False
        geo_field = 'route'
        fields = ('auth_code', 'origin', 'destination', 'origin_name',
            'destination_name', 'creation_date')


class RiverRouteSerializer(ModelSerializer):
    """Serializer to the RiverRoute model."""

    route = GeometryField(source='route', read_only=True)
    origin_name = Field(source='origin.name')
    destination_name = Field(source='destination.name')

    class Meta:
        model = RiverRoute
        id_field = False
        geo_field = 'route'
        fields = ('auth_code', 'origin', 'destination', 'origin_name',
            'destination_name', 'creation_date')
