# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.gis.geos import Point, Polygon, MultiPolygon
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from ..models import State, City, Airport, ShippingPlace
from ..models import RoadRoute, AerialRoute, SeaRoute, RiverRoute


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


class TestShippingPlaceAPI(APITestCase):
    def test_port_list_response(self):
        url = reverse('api:shipping-place-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestFloatsAPI(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('user', 'i@t.com', 'password')
        self.url = reverse('api:create-float')

        self.float_object = {
            'name': 'Port A',
            'category': 'float',
            'point': {
                "type": "Point",
                "coordinates": [0.5, 0.5]
                }
            }
        self.minifloat = {
            'name': 'Port B',
            'category': 'minifloat',
            'point': {
                "type": "Point",
                "coordinates": [0.5, -0.5]
                }
            }

    def test_creation(self):
        self.client.login(username=self.user.username, password='password')

        response = self.client.post(self.url, self.float_object, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(self.url, self.minifloat, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_unlogged_response(self):
        response = self.client.post(self.url, self.minifloat, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_creation(self):
        port_a = {
            'name': 'Port A',
            'category': 'seaport',
            'point': {
                "type": "Point",
                "coordinates": [0.5, 0.5]
                }
            }
        port_b = {
            'name': 'Port B',
            'category': 'riverport',
            'point': {
                "type": "Point",
                "coordinates": [0.5, -0.5]
                }
            }
        self.client.login(username=self.user.username, password='password')

        response = self.client.post(self.url, port_a, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.url, port_b, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestAirportAPI(APITestCase):

    def setUp(self):
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
                "coordinates": [-0.5, -0.5]
                }
            }

        self.url = reverse('api:airport-list')
        self.client.login(username=self.user.username, password='password')
        self.client.post(self.url, self.airport_a, format='json')
        self.client.post(self.url, self.airport_b, format='json')

    def test_airport_creation(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 2)

    def test_bbox_filter(self):

        response = self.client.get(self.url, {'in_bbox': '0,0,1,1'},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 1)

        response = self.client.get(self.url, {'in_bbox': '-1,-1,0,0'},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 1)

    def test_name_filter(self):

        response = self.client.get(self.url, {'name': 'B'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 1)

        response = self.client.get(self.url, {'name': 'airport'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['features']), 2)


class TestRoadRouteAPI(APITestCase):

    def setUp(self):
        poly1 = Polygon([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]])
        self.state1 = State(name='One', code='01', geom=MultiPolygon(poly1))
        self.state1.save()

        poly2 = Polygon([[0, 0], [0, -1], [1, -1], [1, 0], [0, 0]])
        self.state2 = State(name='Two', code='02', geom=MultiPolygon(poly2))
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

        self.user = User.objects.create_user('user', 'i@t.com', 'password')

        self.data = {
            'states': [self.state1.code, self.state2.code],
            'auth_code': '123abc',
            'roads': 'BR-101; BA-001',
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

        auth_code = RoadRoute.objects.all()[0].auth_code
        url = reverse('api:road-route-detail', args=[auth_code])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_road_route_creation(self):
        data = {
            'states': [self.state1.code, self.state2.code],
            'auth_code': '123abc',
            'roads': 'BR-101; BA-001',
            'geom': {
                "type": "LineString",
                "coordinates": [[0.5, 0.5], [2, 2]]
                }
            }

        data_b = {
            'states': [],
            'auth_code': 'jsh123',
            'roads': 'BR-101; BA-001',
            'geom': {
                "type": "LineString",
                "coordinates": [[0.5, 0.5], [2, 2]]
                }
            }

        url = reverse('api:road-route-list')
        self.client.login(username=self.user.username, password='password')

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(url, data_b, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(RoadRoute.objects.all().count(), 0)


class TestAerialRouteAPI(APITestCase):

    def setUp(self):
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
        self.airport_c = {
            'name': "Airport c",
            'geom': {
                "type": "Point",
                "coordinates": [2, -2]
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
            'auth_code': '123abc',
            'origin': id_a,
            'destination': id_b
            }
        url = reverse('api:aerial-route-list')
        response = self.client.post(url, aerial_route, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        auth_code = AerialRoute.objects.all()[0].auth_code
        url = reverse('api:aerial-route-detail', args=[auth_code])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_aerial_route_creation(self):
        url = reverse('api:airport-list')
        self.client.login(username=self.user.username, password='password')

        response = self.client.post(url, self.airport_a, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        id_a = Airport.objects.all()[0].id

        aerial_route_c = {
            'auth_code': '123a',
            'origin': id_a,
            'destination': id_a
            }
        response = self.client.post(url, aerial_route_c, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(AerialRoute.objects.all().count(), 0)


class TestSeaRouteAPI(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('user', 'i@t.com', 'password')

        self.port_a = {
            'name': 'Port A',
            'category': 'float',
            'point': {
                "type": "Point",
                "coordinates": [0.5, 0.5]
                }
            }
        self.port_b = {
            'name': 'Port B',
            'category': 'minifloat',
            'point': {
                "type": "Point",
                "coordinates": [0.5, -0.5]
                }
            }
        self.sea_basin = ShippingPlace.objects.create(name='Basin 1',
            category='seabasin',
            polygon=Polygon([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]))

    def test_sea_route_list(self):
        url = reverse('api:sea-route-list')
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlogged_sea_route(self):
        url = reverse('api:sea-route-list')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_sea_route_creation(self):
        url = reverse('api:create-float')
        self.client.login(username=self.user.username, password='password')

        response = self.client.post(url, self.port_a, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(url, self.port_b, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        sea_basin, port_a, port_b = [item.id for item in ShippingPlace.objects.all()]
        sea_route = {
            'auth_code': '123abc',
            'origin': port_a,
            'destination': port_b
            }
        url = reverse('api:sea-route-list')
        response = self.client.post(url, sea_route, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        auth_code = SeaRoute.objects.all()[0].auth_code
        url = reverse('api:sea-route-detail', args=[auth_code])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        sea_route = {
            'auth_code': '12345abc',
            'origin': sea_basin,
            'destination': sea_basin
            }
        url = reverse('api:sea-route-list')
        response = self.client.post(url, sea_route, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestRiverRouteAPI(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user('user', 'i@t.com', 'password')

        ShippingPlace.objects.create(name="A",
            category='riverport',
            point=Point([0.5, 0.5]))

        ShippingPlace.objects.create(name='Basin 1',
            category='riverbasin',
            polygon=Polygon([[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]))

    def test_river_route_list(self):
        url = reverse('api:river-route-list')
        self.client.login(username=self.user.username, password='password')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlogged_river_route(self):
        url = reverse('api:river-route-list')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_river_route_creation(self):
        self.client.login(username=self.user.username, password='password')
        basin, port = [item.id for item in ShippingPlace.objects.all()]

        river_route = {
            'auth_code': '123abc',
            'origin': port,
            'destination': basin
            }
        url = reverse('api:river-route-list')
        response = self.client.post(url, river_route, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        auth_code = RiverRoute.objects.all()[0].auth_code
        url = reverse('api:river-route-detail', args=[auth_code])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        river_route = {
            'auth_code': '12345abc',
            'origin': basin,
            'destination': basin
            }
        url = reverse('api:river-route-list')
        response = self.client.post(url, river_route, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
