# -*- coding: utf-8 -*-
from cela.models import Cela
from django.shortcuts import render
from django.shortcuts import render,get_object_or_404,redirect

def ruscView(request):

    celas = Cela.objects.exclude(tipus='X')
    notif=[]

    if request.user.is_authenticated():
        notif = request.user.notifications.unread()


    #si ja esta dins de una cela permetem que pugui tornar
    cela_pk = request.session.get('cell', 'NoCell')
    if (cela_pk != 'NoCell'):
        cela = Cela.objects.filter(pk=cela_pk).first()
        return render(request,"rusc.html", {'celas':celas,'cela':cela,'notifications': notif})
    else:
        return render(request,"rusc.html", {'celas':celas,'notifications': notif})




