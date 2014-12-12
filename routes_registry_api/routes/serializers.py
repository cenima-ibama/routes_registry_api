# -*- coding: utf-8 -*-
from django.utils.translation import ugettext, ugettext_lazy as _

from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework.serializers import Field, SlugRelatedField

from .models import State, Port, Airport
from .models import RoadRoute, AerialRoute, AquaticRoute


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
    states = SlugRelatedField(many=True, read_only=False, slug_field='code')

    class Meta:
        model = RoadRoute
        geo_field = 'geom'
        fields = ('id', 'company', 'states', 'creation_date')

    def validate(self, attrs):
        if len(attrs['states']) > 0:
            states = State.objects.filter(code__in=attrs['states']).unionagg()
            if attrs['geom'].within(states) is False:
                raise ValidationError(_('Route is not within the allowed states.'))
            else:
                return attrs
        else:
            raise ValidationError(_('States field can not be empty.'))
        return attrs


class AerialRouteSerializer(ModelSerializer):
    route = Field(source='route')
    states = SlugRelatedField(many=True, read_only=False, slug_field='code')

    class Meta:
        model = AerialRoute
        fields = ('id', 'company', 'states', 'origin', 'destination', 'route',
            'creation_date')

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
    route = Field(source='route')
    states = SlugRelatedField(many=True, read_only=False, slug_field='code')

    class Meta:
        model = AquaticRoute
        fields = ('id', 'company', 'states', 'origin', 'destination', 'route',
            'creation_date')

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