from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from cela import views

urlpatterns = patterns('',
        url(r'^(?P<cela>\d+)/$', views.celaview,name='cela'),
        url(r'^nou/$', login_required(views.celaCreateView.as_view()) ,name='cela_nova'),
        url(r'^nouusuari/$', login_required(views.peticioAcces) ,name='acces_cela'),
        url(r'^modcela/(?P<pk>\d+)/$', login_required(views.celaUpdateView.as_view()) ,name='edicio_cela'),
        url(r'^modepost/$', login_required(views.moderacioPostView) ,name='mode_post'),
        url(r'^modeusers/$', login_required(views.acceptar_usuari) ,name='mode_usuaris'),
        url(r'^convidar/$', login_required(views.cela_convidar ),name='convidar_usu_cela'),
        url(r'^users/$', login_required(views.usuaris_cela) ,name='usuaris_cela'),
        url(r'^changecell/(?P<cela>\d+)/url/(?P<url>\w+)/$', views.celachange, name='canviar_cela'),
        url(r'^visual/$', login_required(views.visual) ,name='visual'),
        url(r'^visualPost/$', login_required(views.visualPost),name='visualPost'),
        url(r'^tesauro_jerarquic_json/', views.tesauro_jerarquic_json, name='tesauro_jerarquic_json'),
        url(r'^tesauro_jerarquic/', login_required(views.tesauro_jerarquic), name='tesauro_jerarquic'),
        url(r'^network/', login_required(views.network), name='network'),
        url(r'^visualcelas/', views.VisualCelas, name='VisualCelas'),
        url(r'^missatge_cela/', login_required(views.missatge_cela), name='missatge_cela'),
)