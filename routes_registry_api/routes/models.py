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


class Route(models.Model):

    company = models.ForeignKey(Company)
    geom = models.LineStringField(srid=4674)
    objects = models.GeoManager()

    def __str__(self):
        return '%s' % self.id

    def clean(self):
        if self.geom.within(self.company.states.unionagg()) is False:
            raise ValidationError(
                _('Route is not within the company allowed states.')
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Route, self).save(*args, **kwargs)