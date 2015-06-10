from .models import Recurs
from django.shortcuts import render, redirect,get_object_or_404
from etiqueta.models import Etiqueta
from cela.models import Cela


def recursview(request,pk):
    cela_pk = request.session.get('cell', 'NoCell')
    if cela_pk == 'NoCell':
        redirect('/rusc')
    cela = get_object_or_404(Cela, pk=cela_pk)

    recurs = Recurs.objects.filter(pk=pk,cela= cela).exclude(moderacio='R').first()

    return render(request, "recurs.html",{'recurs': recurs,'cela':cela})


def zonarecurs(request):
    cela_pk = request.session.get('cell', 'NoCell')
    if cela_pk == 'NoCell':
        redirect('/rusc')
    cela = get_object_or_404(Cela, pk=cela_pk)
    zona_recursos = Etiqueta.objects.filter(tipologia='M',cela= cela)

    return render(request, "zonarecurs.html",{'zona_recursos': zona_recursos,'cela':cela})


def zonaview(request,pkzona):
    cela_pk = request.session.get('cell', 'NoCell')
    if cela_pk == 'NoCell':
        redirect('/rusc')
    cela = get_object_or_404(Cela, pk=cela_pk)
    recursos = Recurs.objects.filter(etiquetes=pkzona,cela= cela).exclude(moderacio='R')

    return render(request, "zona.html",{'recursos': recursos,'cela':cela})