# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from rest_framework.urlpatterns import format_suffix_patterns

from .views import StateDetail
from .views import CompanyList, CompanyDetail
from .views import RouteList, RouteDetail


urlpatterns = patterns('',
    url(r'^state/(?P<pk>[0-9]+)/$', StateDetail.as_view(), name='state-detail'),
    url(r'^companies/', CompanyList.as_view(), name='company-list'),
    url(r'^company/(?P<pk>[0-9]+)/$', CompanyDetail.as_view(), name='company-detail'),
    url(r'^route/(?P<pk>[0-9]+)/$', RouteDetail.as_view(), name='route-detail'),
    url(r'^routes/', RouteList.as_view(), name='route-list'),
)

urlpatterns = format_suffix_patterns(urlpatterns)