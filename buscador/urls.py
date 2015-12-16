# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from buscador import views

urlpatterns = patterns('',
        url(r'^$', login_required(views.buskadorCela) ,name='busk'),

)