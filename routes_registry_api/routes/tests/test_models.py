# -*- coding: utf-8 -*-
from django.test import TestCase
from django.contrib.gis.geos import Polygon, MultiPolygon, LineString, Point

from ..models import State, Port, Airport
from ..models import RoadRoute, AerialRoute, AquaticRoute


class TestRoadRoute(TestCase):

    def setUp(self):
        poly1 = Polygon([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]])
        self.state1 = State(name='State One', code='01', geom=MultiPolygon(poly1))
        self.state1.save()

        poly2 = Polygon([[0, 0], [0, -1], [1, -1], [1, 0], [0, 0]])
        self.state2 = State(name='State Two', code='02', geom=MultiPolygon(poly2))
        self.state2.save()

    def test_state_creation(self):
        self.assertEqual(self.state1.__str__(), '01')
        self.assertEqual(State.objects.all().count(), 2)

    def test_road_route_creation(self):
        valid_route = RoadRoute(
            geom=LineString([0.5, 0.5], [0.5, -0.5]),
            company=1
            )
        valid_route.save()
        self.state1.roadroute_set.add(valid_route)
        self.state2.roadroute_set.add(valid_route)

        self.assertEqual(valid_route.__str__(), '%s' % valid_route.id)
        self.assertTrue(valid_route.valid())
        self.assertEqual(RoadRoute.objects.all().count(), 1)

    def test_invalid_road_route_creation(self):
        invalid_route = RoadRoute(
            geom=LineString([0.5, 0.5], [2, 2]),
            company=1
            )
        invalid_route.save()
        self.state1.roadroute_set.add(invalid_route)
        self.state2.roadroute_set.add(invalid_route)

        self.assertEqual(invalid_route.__str__(), '%s' % invalid_route.id)
        self.assertFalse(invalid_route.valid())
        self.assertEqual(RoadRoute.objects.all().count(), 1)


class TestAerialRoute(TestCase):

    def setUp(self):
        poly1 = Polygon([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]])
        self.state1 = State(name='State One', code='01', geom=MultiPolygon(poly1))
        self.state1.save()

        poly2 = Polygon([[0, 0], [0, -1], [1, -1], [1, 0], [0, 0]])
        self.state2 = State(name='State Two', code='02', geom=MultiPolygon(poly2))
        self.state2.save()

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
            company=1
            )
        valid_route.save()
        self.state1.aerialroute_set.add(valid_route)
        self.state2.aerialroute_set.add(valid_route)

        self.assertEqual(valid_route.__str__(), '%s' % valid_route.id)
        self.assertEqual(valid_route.route(),
            '%s - %s' % (valid_route.origin.name, valid_route.destination.name)
            )
        self.assertTrue(valid_route.valid())

        #with self.assertRaises(ValidationError):
            #AerialRoute.objects.create(
                #origin=self.airport_a,
                #destination=self.airport_c,
                #states=State.objects.all(),
                #company=1
                #)

        #with self.assertRaises(ValidationError):
            #AerialRoute.objects.create(
                #origin=self.airport_a,
                #destination=self.airport_a,
                #states=State.objects.all(),
                #company=1
                #)

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
            company=1
            )
        valid_route.save()
        self.state1.aquaticroute_set.add(valid_route)
        self.state2.aquaticroute_set.add(valid_route)

        self.assertEqual(valid_route.__str__(), '%s' % valid_route.id)
        self.assertEqual(valid_route.route(),
            '%s - %s' % (valid_route.origin.name, valid_route.destination.name)
            )

        #with self.assertRaises(ValidationError):
            #AquaticRoute.objects.create(
                #origin=self.port_a,
                #destination=self.port_c,
                #states=State.objects.all(),
                #company=1
                #)

        #with self.assertRaises(ValidationError):
            #AquaticRoute.objects.create(
                #origin=self.port_a,
                #destination=self.port_a,
                #states=State.objects.all(),
                #company=1
                #)

        self.assertEqual(AquaticRoute.objects.all().count(), 1)
