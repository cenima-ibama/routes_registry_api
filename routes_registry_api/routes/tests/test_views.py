# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import Polygon, MultiPolygon
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status

from ..models import State, Company, RoadRoute


class TestAPIAuthURL(TestCase):

    def test_api_auth_response(self):
        url = reverse('rest_framework:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestCompanyAPI(APITestCase):

    def setUp(self):
        self.data = {"name": "Global"}
        self.user = User.objects.create_user('user', 'i@t.com', 'password')
        self.url = reverse('api:company-list')

    def test_company_list_response(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(self.url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.login(username=self.user.username, password='password')
        self.client.post(self.url, self.data, format='json')

    def test_company_detail_response(self):
        self.client.login(username=self.user.username, password='password')
        self.client.post(self.url, self.data, format='json')

        url = reverse('api:company-detail', args=[1])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestStateAPI(APITestCase):

    def test_state_detail_response(self):
        poly1 = Polygon([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]])
        state = State(name='State One', code='01', geom=MultiPolygon(poly1))
        state.save()
        url = reverse('api:state-detail', args=[state.pk])
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
        self.company = Company.objects.create(name="Global")

        poly1 = Polygon([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]])
        state1 = State(name='State One', code='01', geom=MultiPolygon(poly1))
        state1.save()
        state1.company_set.add(self.company)

        poly2 = Polygon([[0, 0], [0, -1], [1, -1], [1, 0], [0, 0]])
        state2 = State(name='State Two', code='02', geom=MultiPolygon(poly2))
        state2.save()
        state2.company_set.add(self.company)

        self.user = User.objects.create_user('user', 'i@t.com', 'password')

        self.data = {
            'company': self.company.id,
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

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = reverse('api:road-route-detail', args=[1])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_road_route_creation(self):
        data = {
            'company': self.company.id,
            'geom': {
                "type": "LineString",
                "coordinates": [[0.5, 0.5], [2, 2]]
                }
            }

        url = reverse('api:road-route-list')
        self.client.login(username=self.user.username, password='password')
        with self.assertRaises(ValidationError):
            self.client.post(url, data, format='json')
        self.assertEqual(RoadRoute.objects.all().count(), 0)