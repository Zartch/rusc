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
        url(r'^users/$', views.usuaris_cela ,name='usuaris_cela'),
)