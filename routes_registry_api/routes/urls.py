# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import StateDetail
from .views import CompanyList, CompanyDetail
from .views import RoadRouteList, RoadRouteDetail


urlpatterns = patterns('',
    url(r'^state/(?P<pk>[0-9]+)/$',
        StateDetail.as_view(),
        name='state-detail'),
    url(r'^companies/',
        CompanyList.as_view(),
        name='company-list'),
    url(r'^company/(?P<pk>[0-9]+)/$',
        CompanyDetail.as_view(),
        name='company-detail'),
    url(r'^road-routes/',
        RoadRouteList.as_view(),
        name='road-route-list'),
    url(r'^road-route/(?P<pk>[0-9]+)/$',
        RoadRouteDetail.as_view(),
        name='road-route-detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)