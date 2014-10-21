# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import Polygon, MultiPolygon
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from rest_framework.test import APITestCase
from rest_framework import status

from ..models import State, Company, RoadRoute


class TestRouteAPI(APITestCase):

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
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_road_route_creation(self):
        url = reverse('api:road-route-list')
        self.client.login(username=self.user.username, password='password')
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RoadRoute.objects.all().count(), 1)

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