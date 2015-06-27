# -*- coding: utf-8 -*-
from .models import Etiqueta, Tesauro
from post.models import Post,Vote, folksonomia
from cela.models import Cela, get_cela
from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q

def etiquetaview(request,etq):
    cela = get_cela(request)
    etiqueta = Etiqueta.objects.filter(pk=etq, cela = cela).first()
    posts_relacionats = Post.with_votes.get_queryset().filter(etiquetes = etiqueta, cela = cela.pk).exclude(moderacio='R')

    if not request.user.is_anonymous():
        voted = Vote.objects.filter(voter=request.user)
        voted = voted.values_list('post_id', flat=True)
    else:
        voted= []

    tesauros = Tesauro.objects.filter(Q(etq1=etiqueta)|Q(etq2=etiqueta))
    # d = dict()
    # for post_rel in posts_relacionats:
    #     a=post_rel.folksonomia(etiqueta)
    #     for key,value in a.items():
    #         if key in d:
    #             #suma els values
    #             val = d[key]
    #             val = val + value
    #             d[key] = val
    #         else:
    #             d[key]= value

    d = folksonomia(posts_relacionats)
    sorted_x = sorted(d, key=d.get)


    return render(request,"etiqueta.html", {'etiqueta':etiqueta, 'posts_rel': d, 'tesauros':tesauros, 'cela': cela, 'voted':voted, 'posts_relacionats': posts_relacionats})

def todoview(request):
    cela = get_cela(request)
    etiqueta = Etiqueta.objects.filter(nom='ToDo', cela = cela)
    posts = Post.objects.filter(etiquetes=etiqueta, cela = cela)

    return render(request,"toDo.html", {'posts':posts, 'cela': cela})

def feinafeta(request,pkpost):
    cela = get_cela(request)
    todo = Etiqueta.objects.get(nom='ToDo', cela = cela)
    todo_post = Post.objects.filter(pk=pkpost, cela = cela).first()
    todo_post.etiquetes.remove(todo)

    posts = Post.objects.filter(etiquetes=todo, cela = cela)

    return render(request,"toDo.html", {'posts':posts, 'cela': cela})


