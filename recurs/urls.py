from django.conf.urls import patterns, url



from recurs import views

urlpatterns = patterns('',
    url(r'^/zona/(?P<pkzona>\w+)$', views.zonaview, name='zonaview'),
    url(r'^(?P<pk>\d+)$', views.recursview, name='recurs'),
    url(r'^$', views.zonarecurs, name='zonarecurs'),

    url(r'^zona/(?P<pkzona>\w+)$', views.zonaview,name='etiqueta'),
)
