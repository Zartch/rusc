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
from registration.backends.simple.views import RegistrationView
import autocomplete_light
from django.views.generic import RedirectView

autocomplete_light.autodiscover()
admin.autodiscover()

from rusc import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls), name="admin"),
    url(r'^forum/', include('post.urls')),
    url(r'^cela/', include('cela.urls')),
    url(r'^rusc/', views.ruscView, name="rusc"),
    url(r'^usuari/', include('usuari.urls')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    #url(r'^accounts/register/$', RegistrationView.as_view(form_class = ExRegistrationForm), name = 'registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^busk/', include('buscador.urls')),
    url(r'^recurs/', include('recurs.urls')),
    url(r'^etiqueta/', include('etiqueta.urls')),
    url(r'^messages/', include('django_messages.urls')),
    url('^inbox/notifications/', include('notifications.urls')),
    url(r'^faq/', include('rusc.faq.urls')),

    #url(r'^boot/', include('etiqueta.urls')),
    # url(r'^', views.ruscView),
    url(r'^$', RedirectView.as_view(url='/rusc/')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
