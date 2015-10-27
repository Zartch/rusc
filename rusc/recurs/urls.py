from django.conf.urls import patterns, url

from rusc.recurs import views


urlpatterns = patterns('',
    url(r'^zona/(?P<pkzona>\w+)$', views.zonaview, name='zonaview'),
    url(r'^recursos/', views.recursosview, name='recursos'),
    url(r'^(?P<pk>\d+)$', views.recursview, name='recurs'),
    url(r'^$', views.zonarecurs, name='zonarecurs'),
    url(r'^crearecurs/', views.recursCreateView, name='crearecurs'),
#    url(r'^zona/(?P<pkzona>\w+)$', views.zonaview,name='etiqueta'),
)
