# -*- coding: utf-8 -*-
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .serializers import CompanySerializer, StateSerializer, PortSerializer
from .serializers import AirportSerializer, RoadRouteSerializer
from .serializers import AquaticRouteSerializer, AerialRouteSerializer
from .models import State, Company, Port, Airport
from .models import RoadRoute, AerialRoute, AquaticRoute

class StateDetail(RetrieveUpdateDestroyAPIView):
    model = State
    serializer_class = StateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CompanyList(ListCreateAPIView):
    model = Company
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CompanyDetail(RetrieveUpdateDestroyAPIView):
    model = Company
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PortList(ListCreateAPIView):
    model = Port
    serializer_class = PortSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class AirportList(ListCreateAPIView):
    model = Airport
    serializer_class = AirportSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RoadRouteList(ListCreateAPIView):
    model = RoadRoute
    serializer_class = RoadRouteSerializer
    permission_classes = (IsAuthenticated,)


class RoadRouteDetail(RetrieveUpdateDestroyAPIView):
    model = RoadRoute
    serializer_class = RoadRouteSerializer
    permission_classes = (IsAuthenticated,)


class AerialRouteList(ListCreateAPIView):
    model = AerialRoute
    serializer_class = AerialRouteSerializer
    permission_classes = (IsAuthenticated,)


class AerialRouteDetail(RetrieveUpdateDestroyAPIView):
    model = AerialRoute
    serializer_class = AerialRouteSerializer
    permission_classes = (IsAuthenticated,)


class AquaticRouteList(ListCreateAPIView):
    model = AquaticRoute
    serializer_class = AquaticRouteSerializer
    permission_classes = (IsAuthenticated,)


class AquaticRouteDetail(RetrieveUpdateDestroyAPIView):
    model = AquaticRoute
    serializer_class = AquaticRouteSerializer
    permission_classes = (IsAuthenticated,)