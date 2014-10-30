# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import StateDetail
from .views import CompanyList, CompanyDetail
from .views import PortList, AirportList
from .views import RoadRouteList, RoadRouteDetail
from .views import AerialRouteList, AerialRouteDetail


urlpatterns = patterns('',
    url(r'^state/(?P<pk>[0-9]+)/$',
        StateDetail.as_view(),
        name='state-detail'),
    url(r'^companies/$',
        CompanyList.as_view(),
        name='company-list'),
    url(r'^companies/(?P<pk>[0-9]+)/$',
        CompanyDetail.as_view(),
        name='company-detail'),
    url(r'^ports/$',
        PortList.as_view(),
        name='port-list'),
    url(r'^airports/$',
        AirportList.as_view(),
        name='airport-list'),
    url(r'^road-routes/$',
        RoadRouteList.as_view(),
        name='road-route-list'),
    url(r'^road-routes/(?P<pk>[0-9]+)/$',
        RoadRouteDetail.as_view(),
        name='road-route-detail'),
    url(r'^aerial-routes/$',
        AerialRouteList.as_view(),
        name='aerial-route-list'),
    url(r'^aerial-routes/(?P<pk>[0-9]+)/$',
        AerialRouteDetail.as_view(),
        name='aerial-route-detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)