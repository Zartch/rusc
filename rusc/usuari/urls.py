from django.conf.urls import url

from rusc.usuari.views import perfilview,viewuser, UserProfileUpdateView,index,viewuserprofile, moderacioPostView


urlpatterns = [
     url(r'^perfil/$', perfilview, name='mi_perfil'),
     url(r'^perfil/(?P<pk>\d+)$', viewuser, name='perfil'),
     url(r'^userperfil/(?P<pk>\d+)$', viewuserprofile, name='perfil_user'),
     url(r'^(?P<name>\w+)/opcions$',UserProfileUpdateView.as_view(), name='opcions_user'),
     url(r'^m2mselector', index,name= "m2m" ),
     url(r'^moderaciopost', moderacioPostView, name='post_modreracio_usuari'),

]
