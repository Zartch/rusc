"""rusc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin

from django.views.generic import RedirectView
admin.autodiscover()
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    #url(r'^accounts/', include('registration.backends.simple.urls')),
    #url para que no pida el confirmar logout
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^accounts/', include('allauth.urls')),
    #url(r'^accounts/profile/$', TemplateView.as_view(template_name='profile.html')),
    url(r'^accounts/profile/$', RedirectView.as_view(url='/usuari/perfil')),

    url(r'^admin/', include(admin.site.urls), name="admin"),
    url(r'^forum/', include('rusc.post.urls')),
    url(r'^cela/', include('cela.urls')),
    url(r'^rusc/', include('cela.urls')),
    url(r'^usuari/', include('rusc.usuari.urls')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),

    url(r'^busk/', include('buscador.urls')),
    url(r'^recurs/', include('rusc.recurs.urls')),
    url(r'^etiqueta/', include('rusc.etiqueta.urls')),
    url(r'^missatgeModeracio/', include('missatgeModeracio.urls')),
    url(r'^messages/', include('django_messages.urls')),
    url('^inbox/notifications/', include('notifications.urls', namespace="notifications")),
    url(r'^faq/', include('rusc.faq.urls')),
    url(r'^linkMeta/', include('linksMeta.urls')),
    url(r'^resums/', include('rusc.resums.urls')),
    url(r'^ficha/', include('rusc.ficha.urls')),


    #url(r'^boot/', include('etiqueta.urls')), usuari/perfil/
    # url(r'^', views.ruscView),

    url(r'^$', RedirectView.as_view(url='/rusc/')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
