from post.models import Post
from etiqueta.models import Etiqueta
from recurs.models import Recurs
from django.db.models import Q
from cela.models import Cela
from django.shortcuts import render, redirect, get_object_or_404


def buskador(request):

    searchString = request.POST.get('searchString', 0)

    posts = Post.objects.filter(Q(titol__icontains = searchString) | Q(text__icontains = searchString) )
    etiquetes = Etiqueta.objects.filter(Q(nom__icontains = searchString) | Q(descripcio__icontains = searchString))
    recursos = Recurs.objects.filter(Q(url__icontains = searchString))

    # r={'type','var','count'}
    # if 'post' in r:
    #     a={'post'}
    #     a.count = +1
    # else:
    #     r.add()


    return render(request, "buscador.html", {'posts': posts, 'etiquetes': etiquetes, 'recursos': recursos})






def buskadorCela(request):
    cela_pk = request.session.get('cell', 'NoCell')
    if cela_pk == 'NoCell':
        redirect('/rusc')
    cela = get_object_or_404(Cela, pk=cela_pk)

    searchString = request.POST.get('searchString', 0)
    #ToDo Afegir Cela al Buscador, Django no permet Ands i Ors, Construir query manualment
    posts = Post.objects.filter(Q(titol__icontains = searchString) | Q(text__icontains = searchString, cela=cela) )
    etiquetes = Etiqueta.objects.filter( Q(nom__icontains = searchString) | Q(descripcio__icontains = searchString))
    recursos = Recurs.objects.filter(Q(url__icontains = searchString, cela=cela))

    return render(request, "buscador.html", {'posts': posts, 'etiquetes': etiquetes, 'recursos': recursos, 'cela': cela})
