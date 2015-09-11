from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from cela import views

urlpatterns = patterns('',
        url(r'^(?P<cela>\d+)/$', views.celaview,name='cela'),
        url(r'^nou/$', login_required(views.celaCreateView.as_view()) ,name='cela_nova'),
        url(r'^nouusuari/$', views.peticioAcces ,name='acces_cela'),
        url(r'^modcela/(?P<pk>\d+)/$', views.celaUpdateView.as_view() ,name='edicio_cela'),
        url(r'^modepost/$', views.moderacioPostView ,name='mode_post'),
        url(r'^modeusers/$', views.acceptar_usuari ,name='mode_usuaris'),
        url(r'^convidar/$', views.cela_convidar ,name='convidar_usu_cela'),
        url(r'^users/$', views.usuaris_cela ,name='usuaris_cela'),
        url(r'^changecell/(?P<cela>\d+)/url/(?P<url>\w+)/$', views.celachange, name='canviar_cela'),
        url(r'^visual/$', views.visual ,name='visual'),
        url(r'^visualPost/$', views.visualPost,name='visualPost'),
        url(r'^tesauro_jerarquic_json/', views.tesauro_jerarquic_json, name='tesauro_jerarquic_json'),
        url(r'^tesauro_jerarquic/', views.tesauro_jerarquic, name='tesauro_jerarquic'),
        url(r'^network/', views.network, name='network'),
)