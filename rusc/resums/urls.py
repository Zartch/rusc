# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from rusc.resums import views


urlpatterns = patterns('',

    url(r'^/$', views.view_resums, name='resums'),
    url(r'^nou/$', views.resumCreateView, name='nou_resum'),

)