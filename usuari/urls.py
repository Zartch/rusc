from django.conf.urls import include, url
from usuari.views import perfilview,viewuser, UserProfileUpdateView,index

urlpatterns = [
    # Examples:
     url(r'^perfil/$', perfilview, name='mi_perfil'),
     url(r'^perfil/(?P<pk>\d+)$', viewuser, name='perfil'),
     url(r'^(?P<name>\w+)/opcions$',UserProfileUpdateView.as_view(), name='opcions_user'),
     url(r'^m2mselector', index,name= "m2m" ),
]
