from django.contrib.gis.db import models
from django.contrib.gis.geos import MultiPoint
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _


class State(models.Model):

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=2)
    geom = models.MultiPolygonField(srid=4674)
    objects = models.GeoManager()

    def __str__(self):
        return '%s' % self.code


class City(models.Model):

    name = models.CharField(max_length=100)
    state = models.ForeignKey(State)
    ibge_geocode = models.IntegerField()
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
    """Every road route is associated with one authorization code and must be
    within the allowed states of that company.
    """

    auth_code = models.CharField(_('Authorization Code'), max_length=40,
        unique=True)
    states = models.ManyToManyField(State)
    geom = models.LineStringField(srid=4674)
    creation_date = models.DateTimeField(auto_now_add=True)
    objects = models.GeoManager()

    def __str__(self):
        return '%s' % self.id

    class Meta:
        verbose_name = _('Road Route')
        verbose_name_plural = _('Road Routes')


class AerialRoute(models.Model):
    """Every aerial route is associated with one authorization code. The
    airports of origin and destination must be differents and within the
    allowed states of the company.
    """

    auth_code = models.CharField(_('Authorization Code'), max_length=40,
        unique=True)
    states = models.ManyToManyField(State)
    origin = models.ForeignKey(Airport, related_name="route_origin")
    destination = models.ForeignKey(Airport, related_name="route_destination")
    creation_date = models.DateTimeField(auto_now_add=True)
    objects = models.GeoManager()

    def __str__(self):
        return '%s' % self.id

    def route(self):
        return MultiPoint(self.origin.geom, self.destination.geom)

    def clean(self):
        self.clean_fields()

        if self.origin == self.destination:
            raise ValidationError(
                _('The destination airport must be different from the origin.')
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(AerialRoute, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Aerial Route')
        verbose_name_plural = _('Aerial Routes')


class AquaticRoute(models.Model):
    """Every aquatic route is associated with one authorization code. The ports
    of origin and destination must be differents and within the allowed states
    of the company.
    """

    auth_code = models.CharField(_('Authorization Code'), max_length=40,
        unique=True)
    states = models.ManyToManyField(State)
    origin = models.ForeignKey(Port, related_name="route_origin")
    destination = models.ForeignKey(Port, related_name="route_destination")
    creation_date = models.DateTimeField(auto_now_add=True)
    objects = models.GeoManager()

    def __str__(self):
        return '%s' % self.id

    def route(self):
        return MultiPoint(self.origin.geom, self.destination.geom)

    def clean(self):
        self.clean_fields()

        if self.origin == self.destination:
            raise ValidationError(
                _('The destination port must be different from the origin.')
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(AquaticRoute, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Aquatic Route')
        verbose_name_plural = _('Aquatic Routes')