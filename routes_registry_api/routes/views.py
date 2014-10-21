# -*- coding: utf-8 -*-
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import CompanySerializer, StateSerializer, RoadRouteSerializer
from .models import State, Company, RoadRoute


class StateDetail(RetrieveUpdateDestroyAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CompanyList(ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CompanyDetail(RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RoadRouteList(ListCreateAPIView):
    queryset = RoadRoute.objects.all()
    serializer_class = RoadRouteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class RoadRouteDetail(RetrieveUpdateDestroyAPIView):
    queryset = RoadRoute.objects.all()
    serializer_class = RoadRouteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)