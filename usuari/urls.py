__author__ = 'Zartch'
from django.conf.urls import include, url
from usuari.views import perfilview,viewuser

urlpatterns = [
    # Examples:
     url(r'^perfil/$', perfilview, name='mi_perfil'),
     url(r'^perfil/(?P<pk>\d+)$', viewuser, name='perfil'),
]
