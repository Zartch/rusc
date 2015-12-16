# -*- coding: utf-8 -*-
import micawber
from django.http import HttpResponse



def linkMetadata(request):
    providers = micawber.bootstrap_basic()
    link =  request.POST.get('Link')
    linkMetadata =providers.request(link)

    return HttpResponse(linkMetadata['title'])