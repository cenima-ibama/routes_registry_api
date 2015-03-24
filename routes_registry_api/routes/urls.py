# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import StateDetail, AirportList
from .views import ShippingPlaceList, CreateFloatsView
from .views import RoadRouteList, RoadRouteDetail
from .views import AerialRouteList, AerialRouteDetail
from .views import SeaRouteList, SeaRouteDetail
from .views import RiverRouteList, RiverRouteDetail


urlpatterns = patterns('',
    url(r'^state/(?P<code>\w+)/$',
        StateDetail.as_view(),
        name='state-detail'),
    url(r'^airports/$',
        AirportList.as_view(),
        name='airport-list'),

    ### shipping place get and post urls
    url(r'^shipping-places/$',
        ShippingPlaceList.as_view(),
        name='shipping-place-list'),
    url(r'^create-float/$',
        CreateFloatsView.as_view(),
        name='create-float'),

    ### road routes urls
    url(r'^road-routes/$',
        RoadRouteList.as_view(),
        name='road-route-list'),
    url(r'^road-routes/(?P<auth_code>\w+)/$',
        RoadRouteDetail.as_view(),
        name='road-route-detail'),

    ### aerial routes urls
    url(r'^aerial-routes/$',
        AerialRouteList.as_view(),
        name='aerial-route-list'),
    url(r'^aerial-routes/(?P<auth_code>\w+)/$',
        AerialRouteDetail.as_view(),
        name='aerial-route-detail'),

    ### sea routes urls
    url(r'^sea-routes/$',
        SeaRouteList.as_view(),
        name='sea-route-list'),
    url(r'^sea-routes/(?P<auth_code>\w+)/$',
        SeaRouteDetail.as_view(),
        name='sea-route-detail'),

    ### river routes urls
    url(r'^river-routes/$',
        RiverRouteList.as_view(),
        name='river-route-list'),
    url(r'^river-routes/(?P<auth_code>\w+)/$',
        RiverRouteDetail.as_view(),
        name='river-route-detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
