# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import StateDetail
from .views import ShippingPlaceList, AirportList
from .views import RoadRouteList, RoadRouteDetail
from .views import AerialRouteList, AerialRouteDetail
from .views import AquaticRouteList, AquaticRouteDetail


urlpatterns = patterns('',
    url(r'^state/(?P<code>\w+)/$',
        StateDetail.as_view(),
        name='state-detail'),
    url(r'^shipping-place/$',
        ShippingPlaceList.as_view(),
        name='shipping-place-list'),
    url(r'^airports/$',
        AirportList.as_view(),
        name='airport-list'),

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

    ### aquatic routes urls
    url(r'^aquatic-routes/$',
        AquaticRouteList.as_view(),
        name='aquatic-route-list'),
    url(r'^aquatic-routes/(?P<auth_code>\w+)/$',
        AquaticRouteDetail.as_view(),
        name='aquatic-route-detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
