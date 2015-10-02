
from django.conf.urls import patterns, url

from etiqueta import views
from django.contrib.auth.decorators import login_required

urlpatterns = patterns('',
        url(r'^(?P<etq>\d+)/$', views.etiquetaview,name='etiqueta'),
        url(r'^todo/(?P<pkpost>\d+)$', views.feinafeta, name='feina_feta'),
        url(r'^todo', views.todoview, name='todo'),
        url(r'^tesauronou/$', login_required(views.tesauroCreateView.as_view()) ,name='tesauro_nou'),
        url(r'^modtesauro/(?P<pk>\d+)/$', views.tesauroUpdateView.as_view() ,name='mod_tesauro'),
        url(r'^deltesauro/(?P<pk>\d+)/$', views.tesauroDeleteView.as_view() ,name='delete_tesauro'),
)