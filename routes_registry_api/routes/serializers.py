# -*- coding: utf-8 -*-
from django.utils.translation import ugettext, ugettext_lazy as _

from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework_gis.fields import GeometryField
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.serializers import Field, SlugRelatedField

from .models import State, Port, Airport
from .models import RoadRoute, AerialRoute, AquaticRoute


class StateSerializer(GeoFeatureModelSerializer):
    """Serializer to the State model"""

    class Meta:
        model = State
        geo_field = 'geom'
        fields = ('id', 'code', 'name')


class PortSerializer(GeoFeatureModelSerializer):
    """Serializer to the Port model"""

    class Meta:
        model = Port
        geo_field = 'geom'
        fields = ('id', 'name')


class AirportSerializer(GeoFeatureModelSerializer):
    """Serializer to the Airport model"""

    class Meta:
        model = Airport
        geo_field = 'geom'
        fields = ('id', 'name')


class RoadRouteSerializer(GeoFeatureModelSerializer):
    """Serializer to the Road Route model. Only accept route creation if the
    states field is not empty and if the route is within the states geometry."""

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
    """Serializer to the Road Route model. Only accept route creation if the
    states field is not empty and if both the origin and destination airports
    is within the states geometry."""

    route = GeometryField(source='route', read_only=True)
    origin_name = Field(source='origin.name')
    destination_name = Field(source='destination.name')
    states = SlugRelatedField(many=True, read_only=False, slug_field='code')

    class Meta:
        model = AerialRoute
        id_field = False
        geo_field = 'route'
        fields = ('auth_code', 'states', 'origin', 'destination', 'origin_name',
            'destination_name', 'creation_date')

    def validate(self, attrs):
        if len(attrs['states']) > 0:
            states = State.objects.filter(code__in=attrs['states']).unionagg()
            origin = attrs['origin'].geom
            destination = attrs['destination'].geom
            if origin.within(states) and destination.within(states) is False:
                raise ValidationError(
                    _('Origin or Destination is not within the allowed states.')
                    )
            else:
                return attrs
        else:
            raise ValidationError(_('States field can not be empty.'))


class AquaticRouteSerializer(ModelSerializer):
    """Serializer to the Road Route model. Only accept route creation if the
    states field is not empty and if both the origin and destination airports
    is within the states geometry."""

    route = GeometryField(source='route', read_only=True)
    origin_name = Field(source='origin.name')
    destination_name = Field(source='destination.name')
    states = SlugRelatedField(many=True, read_only=False, slug_field='code')

    class Meta:
        model = AquaticRoute
        id_field = False
        geo_field = 'route'
        fields = ('auth_code', 'states', 'origin', 'destination', 'origin_name',
            'destination_name', 'creation_date')

    def validate(self, attrs):
        if len(attrs['states']) > 0:
            states = State.objects.filter(code__in=attrs['states']).unionagg()
            origin = attrs['origin'].geom
            destination = attrs['destination'].geom
            if origin.within(states) and destination.within(states) is False:
                raise ValidationError(
                    _('Origin or Destination is not within the allowed states.')
                    )
            else:
                return attrs
        else:
            raise ValidationError(_('States field can not be empty.'))