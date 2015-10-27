from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from rusc.etiqueta import views

urlpatterns = patterns('',
        url(r'^(?P<etq>\d+)/$', login_required(views.etiquetaview),name='etiqueta'),
        url(r'^modtesauro/(?P<pk>\d+)/$', views.tesauroUpdateView.as_view() ,name='mod_tesauro'),
        url(r'^(?P<nometq>[-\w]+)/(?P<nomcela>[-\w]+)/$', login_required(views.nometiquetaview),name='nom_etiqueta'),
        url(r'^todo/(?P<pkpost>\d+)$', views.feinafeta, name='feina_feta'),
        url(r'^todo', views.todoview, name='todo'),
        url(r'^tesauronou/$', login_required(views.tesauroCreateView.as_view()) ,name='tesauro_nou'),
        url(r'^deltesauro/(?P<pk>\d+)/$', views.tesauroDeleteView.as_view() ,name='delete_tesauro'),
)