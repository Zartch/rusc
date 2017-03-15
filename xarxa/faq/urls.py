# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from xarxa.faq import views


urlpatterns = patterns('',
        url(r'^$', views.faqview ,name='faq'),
        url(r'^newfaq/$', login_required(views.faqCreateView.as_view()) ,name='faq_nova'),
        url(r'^modfaq/(?P<pk>\d+)/$', login_required(views.faqUpdateView.as_view()) ,name='faq_modif'),
)