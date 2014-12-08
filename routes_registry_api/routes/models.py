from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _


class State(models.Model):

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=2)
    geom = models.MultiPolygonField(srid=4674)
    objects = models.GeoManager()

    def __str__(self):
        return '%s' % self.name


class Port(models.Model):

    name = models.CharField(max_length=255)
    geom = models.PointField(srid=4674)
    objects = models.GeoManager()

    def __str__(self):
        return '%s' % self.name


class Airport(models.Model):

    name = models.CharField(max_length=255)
    geom = models.PointField(srid=4674)
    objects = models.GeoManager()

    def __str__(self):
        return '%s' % self.name


class RoadRoute(models.Model):
    """Every road route is associated with a company and must be within the
    allowed states of that company."""

    company = models.IntegerField()
    states = models.ManyToManyField(State)
    geom = models.LineStringField(srid=4674)
    creation_date = models.DateTimeField(auto_now_add=True)
    objects = models.GeoManager()

    def __str__(self):
        return '%s' % self.id

    def valid(self):
        if self.geom.within(self.states.unionagg()):
            return True
        else:
            return False

    class Meta:
        verbose_name = _('Road Route')
        verbose_name_plural = _('Road Routes')


class AerialRoute(models.Model):
    """Every aerial route is associated with a company. The airports of origin
    and destination must be differents and within the allowed states of
    the company."""

    company = models.IntegerField()
    states = models.ManyToManyField(State)
    origin = models.ForeignKey(Airport, related_name="route_origin")
    destination = models.ForeignKey(Airport, related_name="route_destination")
    creation_date = models.DateTimeField(auto_now_add=True)
    objects = models.GeoManager()

    def __str__(self):
        return '%s' % self.id

    def route(self):
        return '%s - %s' % (self.origin.name, self.destination.name)

    def valid(self):
        if (self.origin.geom.within(self.states.unionagg()) and
            self.destination.geom.within(self.states.unionagg())):
            return True
        else:
            return False

    class Meta:
        verbose_name = _('Aerial Route')
        verbose_name_plural = _('Aerial Routes')


class AquaticRoute(models.Model):
    """Every aquatic route is associated with a company. The ports of origin
    and destination must be differents and within the allowed states of
    the company."""

    company = models.IntegerField()
    states = models.ManyToManyField(State)
    origin = models.ForeignKey(Port, related_name="route_origin")
    destination = models.ForeignKey(Port, related_name="route_destination")
    creation_date = models.DateTimeField(auto_now_add=True)
    objects = models.GeoManager()

    def __str__(self):
        return '%s' % self.id

    def route(self):
        return '%s - %s' % (self.origin.name, self.destination.name)

    def valid(self):
        if (self.origin.geom.within(self.states.unionagg()) and
            self.destination.geom.within(self.states.unionagg())):
            return True
        else:
            return False

    class Meta:
        verbose_name = _('Aquatic Route')
        verbose_name_plural = _('Aquatic Routes')