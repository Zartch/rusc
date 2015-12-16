# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from missatgeModeracio import views

urlpatterns = patterns('',

        url(r'^missMod/(?P<pk>\d+)/(?P<tipus>\w+)/$', login_required(views.moderacioPost), name='missModeracio'),
        #url(r'^acceptarRebutjarPost/(?P<pkpost>\d+)/(?P<action>\w+)$', login_required(moderacioViews.acceptarRebutjarPost), name='acceptarRebutjarPost'),

)