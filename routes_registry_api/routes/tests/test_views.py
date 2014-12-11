# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import Polygon, MultiPolygon
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status

from ..models import State, Airport, Port
from ..models import RoadRoute, AerialRoute, AquaticRoute


class TestAPIAuthURL(TestCase):

    def test_api_auth_response(self):
        url = reverse('rest_framework:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestStateAPI(APITestCase):

    def test_state_detail_response(self):
        poly1 = Polygon([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]])
        state = State(name='State One', code='01', geom=MultiPolygon(poly1))
        state.save()
        url = reverse('api:state-detail', args=[state.code])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPortAPI(APITestCase):

    def test_port_list_response(self):
        url = reverse('api:port-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAirportAPI(APITestCase):

    def test_airport_list_response(self):
        url = reverse('api:airport-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestRoadRouteAPI(APITestCase):

    def setUp(self):
        poly1 = Polygon([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]])
        self.state1 = State(name='State One', code='01', geom=MultiPolygon(poly1))
        self.state1.save()

        poly2 = Polygon([[0, 0], [0, -1], [1, -1], [1, 0], [0, 0]])
        self.state2 = State(name='State Two', code='02', geom=MultiPolygon(poly2))
        self.state2.save()

        self.user = User.objects.create_user('user', 'i@t.com', 'password')

        self.data = {
            'states': [self.state1.code, self.state2.code],
            'company': 1,
            'geom': {
                "type": "LineString",
                "coordinates": [[0.5, 0.5], [0.5, -0.5]]
                }
            }

    def test_unlogged_response(self):
        url = reverse('api:road-route-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_road_route_creation(self):

        url = reverse('api:road-route-list')
        self.client.login(username=self.user.username, password='password')

        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RoadRoute.objects.all().count(), 1)
        self.assertTrue(response.data['properties']['valid'])

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        pk = RoadRoute.objects.all()[0].pk
        url = reverse('api:road-route-detail', args=[pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        url = reverse('api:road-route-geojson-detail', args=[1])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_road_route_creation(self):
        data = {
            'states': [self.state1.code, self.state2.code],
            'company': 1,
            'geom': {
                "type": "LineString",
                "coordinates": [[0.5, 0.5], [2, 2]]
                }
            }

        url = reverse('api:road-route-list')
        self.client.login(username=self.user.username, password='password')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data['properties']['valid'])
        self.assertEqual(RoadRoute.objects.all().count(), 1)


class TestAerialRouteAPI(APITestCase):

    def setUp(self):
        poly1 = Polygon([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]])
        self.state1 = State(name='State One', code='01', geom=MultiPolygon(poly1))
        self.state1.save()

        poly2 = Polygon([[0, 0], [0, -1], [1, -1], [1, 0], [0, 0]])
        self.state2 = State(name='State Two', code='02', geom=MultiPolygon(poly2))
        self.state2.save()

        self.user = User.objects.create_user('user', 'i@t.com', 'password')

        self.airport_a = {
            'name': "Airport A",
            'geom': {
                "type": "Point",
                "coordinates": [0.5, 0.5]
                }
            }
        self.airport_b = {
            'name': "Airport B",
            'geom': {
                "type": "Point",
                "coordinates": [0.5, -0.5]
                }
            }

    def test_aerial_route_list(self):
        url = reverse('api:aerial-route-list')
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlogged_aerial_route(self):
        url = reverse('api:airport-list')
        response = self.client.post(url, self.airport_a, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_aerial_route_creation(self):
        url = reverse('api:airport-list')
        self.client.login(username=self.user.username, password='password')

        response = self.client.post(url, self.airport_a, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, self.airport_b, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        id_a, id_b = [airport.id for airport in Airport.objects.all()]
        aerial_route = {
            'states': [self.state1.id, self.state2.id],
            'company': 1,
            'origin': id_a,
            'destination': id_b
            }
        url = reverse('api:aerial-route-list')
        response = self.client.post(url, aerial_route, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        pk = AerialRoute.objects.all()[0].pk
        url = reverse('api:aerial-route-detail', args=[pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('api:aerial-route-origin', args=[id_a])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('api:aerial-route-destination', args=[id_a])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAquaticRouteAPI(APITestCase):

    def setUp(self):
        poly1 = Polygon([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]])
        self.state1 = State(name='State One', code='01', geom=MultiPolygon(poly1))
        self.state1.save()

        poly2 = Polygon([[0, 0], [0, -1], [1, -1], [1, 0], [0, 0]])
        self.state2 = State(name='State Two', code='02', geom=MultiPolygon(poly2))
        self.state2.save()

        self.user = User.objects.create_user('user', 'i@t.com', 'password')

        self.port_a = {
            'name': "Port A",
            'geom': {
                "type": "Point",
                "coordinates": [0.5, 0.5]
                }
            }
        self.port_b = {
            'name': "Port B",
            'geom': {
                "type": "Point",
                "coordinates": [0.5, -0.5]
                }
            }

    def test_aquatic_route_list(self):
        url = reverse('api:aquatic-route-list')
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlogged_aquatic_route(self):
        url = reverse('api:port-list')
        response = self.client.post(url, self.port_a, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_aquatic_route_creation(self):
        url = reverse('api:port-list')
        self.client.login(username=self.user.username, password='password')

        response = self.client.post(url, self.port_a, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, self.port_b, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        id_a, id_b = [port.id for port in Port.objects.all()]
        aquatic_route = {
            'states': [self.state1.id, self.state2.id],
            'company': 1,
            'origin': id_a,
            'destination': id_b
            }
        url = reverse('api:aquatic-route-list')
        response = self.client.post(url, aquatic_route, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        pk = AquaticRoute.objects.all()[0].pk
        url = reverse('api:aquatic-route-detail', args=[pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('api:aquatic-route-origin', args=[id_a])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('api:aquatic-route-destination', args=[id_a])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)