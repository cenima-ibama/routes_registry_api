# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import StateDetail
from .views import PortList, AirportList
from .views import RoadRouteList, RoadRouteDetail, RoadRouteGeoJSONDetail
from .views import AerialRouteList, AerialRouteDetail
from .views import AerialRouteOrigin, AerialRouteDestination
from .views import AquaticRouteList, AquaticRouteDetail
from .views import AquaticRouteOrigin, AquaticRouteDestination


urlpatterns = patterns('',
    url(r'^state/(?P<pk>[0-9]+)/$',
        StateDetail.as_view(),
        name='state-detail'),
    url(r'^ports/$',
        PortList.as_view(),
        name='port-list'),
    url(r'^airports/$',
        AirportList.as_view(),
        name='airport-list'),

    ### road routes urls
    url(r'^road-routes/$',
        RoadRouteList.as_view(),
        name='road-route-list'),
    url(r'^road-routes/(?P<pk>[0-9]+)/$',
        RoadRouteDetail.as_view(),
        name='road-route-detail'),
    url(r'^road-routes/(?P<pk>[0-9]+)/geojson/$',
        RoadRouteGeoJSONDetail.as_view(),
        name='road-route-geojson-detail'),

    ### aerial routes urls
    url(r'^aerial-routes/$',
        AerialRouteList.as_view(),
        name='aerial-route-list'),
    url(r'^aerial-routes/(?P<pk>[0-9]+)/$',
        AerialRouteDetail.as_view(),
        name='aerial-route-detail'),
    url(r'^aerial-routes/(?P<pk>[0-9]+)/origin/$',
        AerialRouteOrigin.as_view(),
        name='aerial-route-origin'),
    url(r'^aerial-routes/(?P<pk>[0-9]+)/destination/$',
        AerialRouteDestination.as_view(),
        name='aerial-route-destination'),

    ### aquatic routes urls
    url(r'^aquatic-routes/$',
        AquaticRouteList.as_view(),
        name='aquatic-route-list'),
    url(r'^aquatic-routes/(?P<pk>[0-9]+)/$',
        AquaticRouteDetail.as_view(),
        name='aquatic-route-detail'),
    url(r'^aquatic-routes/(?P<pk>[0-9]+)/origin/$',
        AquaticRouteOrigin.as_view(),
        name='aquatic-route-origin'),
    url(r'^aquatic-routes/(?P<pk>[0-9]+)/destination/$',
        AquaticRouteDestination.as_view(),
        name='aquatic-route-destination'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
