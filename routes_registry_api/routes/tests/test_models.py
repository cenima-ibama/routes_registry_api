# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.gis.geos import Polygon, MultiPolygon, LineString, Point
from django.core.exceptions import ValidationError

from ..models import State, Company, RoadRoute, AerialRoute, AquaticRoute


class TestRoadRoute(TestCase):

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

    def test_company_creation(self):
        self.assertEqual(self.company.__str__(), 'Global')
        self.assertEqual(Company.objects.all().count(), 1)

    def test_state_creation(self):
        self.assertEqual(self.state1.__str__(), 'State One')
        self.assertEqual(State.objects.all().count(), 2)

    def test_road_route_creation(self):
        valid_route = RoadRoute(company=self.company,
            geom=LineString([0.5, 0.5], [0.5, -0.5])
            )
        valid_route.save()
        self.assertEqual(valid_route.__str__(), '%s' % valid_route.id)
        self.assertEqual(RoadRoute.objects.all().count(), 1)

        with self.assertRaises(ValidationError):
            RoadRoute.objects.create(company=self.company,
                geom=LineString([0.5, 0.5], [2, 2])
                )


class TestAerialRoute(TestCase):

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

    def test_aerial_route_creation(self):
        valid_route = AerialRoute(company=self.company,
            origin=Point([0.5, 0.5]),
            destination=Point([0.5, -0.5]),
            )
        valid_route.save()
        self.assertEqual(valid_route.__str__(), '%s' % valid_route.id)
        self.assertEqual(AerialRoute.objects.all().count(), 1)

        with self.assertRaises(ValidationError):
            AerialRoute.objects.create(company=self.company,
                origin=Point([0.5, 0.5]),
                destination=Point([2, 2]),
                )


class TestAquaticRoute(TestCase):

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

    def test_aquatic_route_creation(self):
        valid_route = AquaticRoute(company=self.company,
            origin=Point([0.5, 0.5]),
            destination=Point([0.5, -0.5]),
            )
        valid_route.save()
        self.assertEqual(valid_route.__str__(), '%s' % valid_route.id)
        self.assertEqual(AquaticRoute.objects.all().count(), 1)

        with self.assertRaises(ValidationError):
            AquaticRoute.objects.create(company=self.company,
                origin=Point([0.5, 0.5]),
                destination=Point([2, 2]),
                )