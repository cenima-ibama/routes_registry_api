# -*- coding: utf-8 -*-
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .serializers import CompanySerializer, StateSerializer, PortSerializer
from .serializers import AirportSerializer, RoadRouteSerializer
from .models import State, Company, Port, Airport, RoadRoute


class StateDetail(RetrieveUpdateDestroyAPIView):
    model = State
    serializer_class = StateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CompanyList(ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class PortList(ListCreateAPIView):
    queryset = Port.objects.all()
    serializer_class = PortSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class AirportList(ListCreateAPIView):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CompanyDetail(RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RoadRouteList(ListCreateAPIView):
    queryset = RoadRoute.objects.all()
    serializer_class = RoadRouteSerializer
    permission_classes = (IsAuthenticated,)


class RoadRouteDetail(RetrieveUpdateDestroyAPIView):
    queryset = RoadRoute.objects.all()
    serializer_class = RoadRouteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)