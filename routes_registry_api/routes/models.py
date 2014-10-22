from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext, ugettext_lazy as _


class State(models.Model):

    name = models.CharField(max_length=50)
    code = models.CharField(max_length=2)
    geom = models.MultiPolygonField(srid=4674)
    objects = models.GeoManager()

    def __str__(self):
        return '%s' % self.name


class Company(models.Model):

    name = models.CharField(max_length=255)
    states = models.ManyToManyField(State)
    users = models.ManyToManyField(User)

    def __str__(self):
        return '%s' % self.name

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')


class RoadRoute(models.Model):

    company = models.ForeignKey(Company)
    geom = models.LineStringField(srid=4674)
    objects = models.GeoManager()

    def __str__(self):
        return '%s' % self.id

    def clean(self):
        self.clean_fields()

        if self.geom.within(self.company.states.unionagg()) is False:
            raise ValidationError(
                _('Route is not within the company allowed states.')
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(RoadRoute, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Road Route')
        verbose_name_plural = _('Road Routes')


class AirRoute(models.Model):

    company = models.ForeignKey(Company)
    origin = models.PointField(srid=4674)
    destination = models.PointField(srid=4674)
    objects = models.GeoManager()

    def __str__(self):
        return '%s' % self.id

    def clean(self):
        self.clean_fields()

        if self.origin.within(self.company.states.unionagg()) is False:
            raise ValidationError(
                _('The origin is not within the company allowed states.')
                )

        if self.destination.within(self.company.states.unionagg()) is False:
            raise ValidationError(
                _('The destination is not within the company allowed states.')
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(AirRoute, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Air Route')
        verbose_name_plural = _('Air Routes')


class AerialRoute(models.Model):

    company = models.ForeignKey(Company)
    origin = models.PointField(srid=4674)
    destination = models.PointField(srid=4674)
    objects = models.GeoManager()

    def __str__(self):
        return '%s' % self.id

    def clean(self):
        self.clean_fields()

        if self.origin.within(self.company.states.unionagg()) is False:
            raise ValidationError(
                _('The origin is not within the company allowed states.')
                )

        if self.destination.within(self.company.states.unionagg()) is False:
            raise ValidationError(
                _('The destination is not within the company allowed states.')
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(AerialRoute, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _('Aerial Route')
        verbose_name_plural = _('Aerial Routes')