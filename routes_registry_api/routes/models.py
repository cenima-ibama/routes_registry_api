from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, MultiPoint
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
        return '%s - %s' % (self.name, self.state.code)


class ShippingPlace(models.Model):

    CATEGORY_CHOICES = (
        ('seaport', _('Seaport')),
        ('river_port', _('River port')),
        ('float', _('Float')),
        ('mini_float', _('Mini float')),
        ('sea_basin', _('Sea basin')),
        ('river_basin', _('River basin')),
    )

    name = models.CharField(max_length=255)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    point = models.PointField(srid=4674, null=True, blank=True)
    polygon = models.PolygonField(srid=4674, null=True, blank=True)
    objects = models.GeoManager()

    def __str__(self):
        return '%s' % self.name

    def geom(self):
        if self.category in ['sea_basin', 'river_basin']:
            return self.polygon
        else:
            return self.point

    def clean(self):
        self.clean_fields()
        if self.category in ['sea_basin', 'river_basin']:
            if self.polygon is None:
                raise ValidationError(
                    _("""Polygon field can't be null for objects in the
                        'sea_basin' or 'river_basin' categories.""")
                )
        else:
            if self.point is None:
                raise ValidationError(
                    _("""Point field can't be null for objects in the 'seaport',
                        'river_port', 'float' or 'mini_float' categories.""")
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(ShippingPlace, self).save(*args, **kwargs)


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
    origin = models.ForeignKey(City, blank=True,
        related_name='roadroute_origin')
    destination = models.ForeignKey(City, blank=True,
        related_name='roadroute_destination')
    roads = models.CharField(max_length=255)
    objects = models.GeoManager()

    def __str__(self):
        return '%s' % self.id

    def save(self, *args, **kwargs):
        self.full_clean()
        self.origin = City.objects.get(geom__contains=Point(self.geom[0]))
        self.destination = City.objects.get(geom__contains=Point(self.geom[-1]))
        super(RoadRoute, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Road Route')
        verbose_name_plural = _('Road Routes')


class AerialRoute(models.Model):
    """Every aerial route is associated with one authorization code. The
    airports of origin and destination must be distincts.
    """

    auth_code = models.CharField(_('Authorization Code'), max_length=40,
        unique=True)
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
    origin = models.ForeignKey(ShippingPlace, related_name="route_origin")
    destination = models.ForeignKey(ShippingPlace, related_name="route_destination")
    creation_date = models.DateTimeField(auto_now_add=True)
    objects = models.GeoManager()

    def __str__(self):
        return '%s' % self.id

    def route(self):
        return MultiPoint(self.origin.geom(), self.destination.geom())

    def save(self, *args, **kwargs):
        self.full_clean()
        super(AquaticRoute, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Aquatic Route')
        verbose_name_plural = _('Aquatic Routes')