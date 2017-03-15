__author__ = 'zartch'
from django.conf.urls import patterns, url

from xarxa.ficha import views


urlpatterns = patterns('',

    url(r'^nova/', views.fichaCreateView, name='fichaNew'),
    url(r'^llisat/', views.fichaListView, name='llistatfichas'),

)