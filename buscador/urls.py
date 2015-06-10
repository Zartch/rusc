from django.conf.urls import patterns, url

from buscador import views

urlpatterns = patterns('',
        url(r'^$', views.buskadorCela ,name='busk'),

)