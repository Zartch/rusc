# -*- coding: utf-8 -*-
from .models import Recurs
from django.shortcuts import render, redirect,get_object_or_404
from etiqueta.models import Etiqueta
from cela.models import Cela, get_cela
from post.models import Post
from django.contrib import messages

def recursview(request,pk):

    cela = get_cela(request)
    recurs = Recurs.objects.filter(pk=pk,cela= cela).exclude(moderacio='R').first()
    posts_relacionats = Post.objects.filter(recursos = recurs)

    return render(request, "recurs.html",{'recurs': recurs, 'posts_relacionats':posts_relacionats , 'posts_debat': recurs.post_debat})


def zonarecurs(request):

    cela = get_cela(request)
    zona_recursos = Etiqueta.objects.filter(tipologia='M',cela= cela)
    # noti = {'text':"RecursView", 'type':"succes"}
    return render(request, "zonarecurs.html",{'zona_recursos': zona_recursos})


def zonaview(request,pkzona):

    recursos = Recurs.objects.filter(etiquetes=pkzona,cela= get_cela(request)).exclude(moderacio='R')
    return render(request, "zona.html",{'recursos': recursos})