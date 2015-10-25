from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from linksMeta import views

urlpatterns = patterns('',
        url(r'', login_required(views.linkMetadata) ,name='link_metadata'),

)
