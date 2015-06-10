
from django.conf.urls import patterns, url

from etiqueta import views

urlpatterns = patterns('',
        url(r'^(?P<etq>\d+)/$', views.etiquetaview,name='etiqueta'),
        url(r'^todo/(?P<pkpost>\d+)$', views.feinafeta, name='feina_feta'),
        url(r'^todo', views.todoview, name='todo'),

)