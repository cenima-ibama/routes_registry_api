# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.gis.geos import Polygon, MultiPolygon, LineString
from django.core.exceptions import ValidationError

from ..models import State, Company, Route


class TestRoute(TestCase):

    def setUp(self):
        self.company = Company.objects.create(name="Global")

        poly1 = Polygon([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]])
        self.state1 = State(name='State One', code='01', geom=MultiPolygon(poly1))
        self.state1.save()
        self.state1.company_set.add(self.company)

        poly2 = Polygon([[0, 0], [0, -1], [1, -1], [1, 0], [0, 0]])
        state2 = State(name='State Two', code='02', geom=MultiPolygon(poly2))
        state2.save()
        state2.company_set.add(self.company)

        self.valid_route = Route(company=self.company,
            geom=LineString([0.5, 0.5], [0.5, -0.5])
            )
        self.valid_route.save()

    def test_company_creation(self):
        self.assertEqual(self.company.__str__(), 'Global')
        self.assertEqual(Company.objects.all().count(), 1)

    def test_state_creation(self):
        self.assertEqual(self.state1.__str__(), 'State One')
        self.assertEqual(State.objects.all().count(), 2)

    def test_route_creation(self):
        self.assertEqual(self.valid_route.__str__(), '%s' % self.valid_route.id)
        self.assertEqual(Route.objects.all().count(), 1)

        with self.assertRaises(ValidationError):
            Route.objects.create(company=self.company,
                geom=LineString([0.5, 0.5], [2, 2])
                )