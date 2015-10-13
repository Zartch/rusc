from django.conf.urls import patterns, url
from .views import postCreateView, VoteFormView
from django.contrib.auth.decorators import login_required as auth
from post import views

urlpatterns = patterns('',
    url(r'^post/nou/$', postCreateView ,name='post_nou'),
    url(r'^post/(?P<pk>\d+)/reply/$', postCreateView ,name='post_respon'),
    url(r'^perfil/(?P<pk>\d+)$', views.postView, name='perfil'),
    url(r'^post/(?P<pkpost>\d+)$', views.postView, name='post'),
    url(r'^$', views.forum, name='forum'),
    url(r'^resums/$', views.view_resums, name='resums'),
    url(r'^vote/$', auth(VoteFormView.as_view()), name="vote"),
    url(r'^url/$', views.link_verify),


)