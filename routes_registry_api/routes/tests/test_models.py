# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.gis.geos import Polygon, MultiPolygon, LineString
from django.contrib.gis.geos import Point, MultiPoint
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from ..models import State, City, Port, Airport
from ..models import RoadRoute, AerialRoute, AquaticRoute


class TestRoadRoute(TestCase):

    def setUp(self):
        poly1 = Polygon([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]])
        self.state1 = State(name='State One', code='01', geom=MultiPolygon(poly1))
        self.state1.save()

        poly2 = Polygon([[0, 0], [0, -1], [1, -1], [1, 0], [0, 0]])
        self.state2 = State(name='State Two', code='02', geom=MultiPolygon(poly2))
        self.state2.save()

        poly3 = Polygon([[0, 0], [0, 0.6], [0.6, 0.6], [0.6, 0], [0, 0]])
        self.city1 = City(name='City One', ibge_geocode=1, state=self.state1,
            geom=MultiPolygon(poly3)
            )
        self.city1.save()

        poly4 = Polygon([[0, 0], [0, -0.6], [0.6, -0.6], [0.6, 0], [0, 0]])
        self.city2 = City(name='City Two', ibge_geocode=2, state=self.state2,
            geom=MultiPolygon(poly4)
            )
        self.city2.save()

    def test_state_creation(self):
        self.assertEqual(self.state1.__str__(), '01')
        self.assertEqual(State.objects.all().count(), 2)

    def test_city_creation(self):
        self.assertEqual(self.city1.__str__(), 'City One - 01')
        self.assertEqual(City.objects.all().count(), 2)

    def test_road_route_creation(self):
        valid_route = RoadRoute(
            geom=LineString([0.1, 0.1], [0.1, -0.1]),
            auth_code='123abc',
            roads='BR-101; BA-001'
            )
        valid_route.save()
        self.state1.roadroute_set.add(valid_route)
        self.state2.roadroute_set.add(valid_route)

        self.assertEqual(valid_route.__str__(), '%s' % valid_route.id)
        self.assertEqual(valid_route.origin, self.city1)
        self.assertEqual(valid_route.destination, self.city2)

        with self.assertRaises(ValidationError):
            with transaction.atomic():
                RoadRoute.objects.create(auth_code='123abc',
                    roads='BR-101; BA-001',
                    geom=LineString([0.5, 0.5], [0.5, -0.5])
                    )

        self.assertEqual(RoadRoute.objects.all().count(), 1)


class TestAerialRoute(TestCase):

    def setUp(self):
        self.airport_a = Airport.objects.create(name="A", geom=Point([0.5, 0.5]))
        self.airport_b = Airport.objects.create(name="B", geom=Point([0.5, -0.5]))
        self.airport_c = Airport.objects.create(name="C", geom=Point([2, 2]))

    def test_airport_creation(self):
        self.assertEqual(self.airport_a.__str__(), 'A')
        self.assertEqual(Airport.objects.all().count(), 3)

    def test_aerial_route_creation(self):
        valid_route = AerialRoute(
            origin=self.airport_a,
            destination=self.airport_b,
            auth_code='123abc'
            )
        valid_route.save()

        self.assertEqual(valid_route.__str__(), '%s' % valid_route.id)

        self.assertEqual(valid_route.route(),
            MultiPoint(Point(0.5, 0.5), Point(0.5,-0.5)))

        with self.assertRaises(ValidationError):
            AerialRoute.objects.create(auth_code='123a',
                origin=self.airport_a,
                destination=self.airport_a
            )

        with self.assertRaises(ValidationError):
            AerialRoute.objects.create(auth_code='123abc',
                origin=self.airport_a,
                destination=self.airport_c
            )

        self.assertEqual(AerialRoute.objects.all().count(), 1)


class TestAquaticRoute(TestCase):

    def setUp(self):
        poly1 = Polygon([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]])
        self.state1 = State(name='State One', code='01', geom=MultiPolygon(poly1))
        self.state1.save()

        poly2 = Polygon([[0, 0], [0, -1], [1, -1], [1, 0], [0, 0]])
        self.state2 = State(name='State Two', code='02', geom=MultiPolygon(poly2))
        self.state2.save()

        self.port_a = Port.objects.create(name="A", geom=Point([0.5, 0.5]))
        self.port_b = Port.objects.create(name="B", geom=Point([0.5, -0.5]))
        self.port_c = Port.objects.create(name="C", geom=Point([2, 2]))

    def test_port_creation(self):
        self.assertEqual(self.port_a.__str__(), 'A')
        self.assertEqual(Port.objects.all().count(), 3)

    def test_aquatic_route_creation(self):
        valid_route = AquaticRoute(
            origin=self.port_a,
            destination=self.port_b,
            auth_code='123abc'
            )
        valid_route.save()
        self.state1.aquaticroute_set.add(valid_route)
        self.state2.aquaticroute_set.add(valid_route)

        self.assertEqual(valid_route.__str__(), '%s' % valid_route.id)

        self.assertEqual(valid_route.route(),
            MultiPoint(Point(0.5, 0.5), Point(0.5,-0.5)))

        with self.assertRaises(ValidationError):
            AquaticRoute.objects.create(auth_code='123a',
                origin=self.port_a,
                destination=self.port_a,
            )

        with self.assertRaises(ValidationError):
            AquaticRoute.objects.create(auth_code='123abc',
                origin=self.port_a,
                destination=self.port_c,
            )

        self.assertEqual(AquaticRoute.objects.all().count(), 1)
