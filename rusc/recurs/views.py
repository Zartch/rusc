# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.contrib import messages as notif_messages
from django.utils.datastructures import MultiValueDictKeyError

from .models import Recurs
from rusc.etiqueta.models import Etiqueta
from cela.models import get_cela
from rusc.post.models import Post
from rusc.recurs.forms import RecursForm


def recursview(request,pk):

    cela = get_cela(request)
    recurs = Recurs.objects.filter(pk=pk,cela= cela).exclude(moderacio='R').first()
    posts_relacionats = Post.objects.filter(recursos = recurs)

    return render(request, "recurs.html",{'recurs': recurs, 'posts_relacionats':posts_relacionats , 'posts_debat': recurs.post_debat})

def recursosview(request):

    cela = get_cela(request)
    recursos = Recurs.objects.filter(cela= cela).exclude(moderacio='R')

    return render(request, "recursos.html",{'recursos': recursos})


def zonarecurs(request):

    cela = get_cela(request)
    zona_recursos = Etiqueta.objects.filter(tipologia='M',cela= cela)
    # noti = {'text':"RecursView", 'type':"succes"}
    return render(request, "zonarecurs.html",{'zona_recursos': zona_recursos})


def zonaview(request,pkzona):

    recursos = Recurs.objects.filter(etiquetes=pkzona,cela= get_cela(request)).exclude(moderacio='R')
    return render(request, "zona.html",{'recursos': recursos})

def recursCreateView(request):
    if not request.user.is_authenticated():
            return redirect('auth_login')
    cela= get_cela(request)
    #https://docs.djangoproject.com/en/1.8/topics/http/file-uploads/
    formRecurs = RecursForm(request.POST or None, request= request)

    if formRecurs.is_valid():
        data = formRecurs.cleaned_data
        #handle_uploaded_file(request.FILES['file'])

        #creem el post del recurs
        post_x = Post.objects.create(titol=data['url'], autor = request.user,  text="Discussio del recurs: "+ data['descripcio'], cela=get_cela(request))

        try:
            aj = request.FILES['adjunt']
            rec = Recurs.objects.create(descripcio=data['descripcio'],
                                        url=data['url'],
                                        cela= cela,
                                        autor=request.user,
                                        adjunt=request.FILES['adjunt'],
                                        post_debat = post_x)

        except MultiValueDictKeyError:
            rec = Recurs.objects.create(descripcio=data['descripcio'],
                                        url=data['url'],
                                        cela= cela,
                                        autor=request.user,
                                        post_debat = post_x)
        #Associem el recurs al debat
        post_x.recursos.add(rec)
        post_x.save()

        #Recollim les variables per a crear les etiquetes  asociales al recurs
        #etqAdd = request.POST.get('etiquetes-autocomplete', 0)
        etqlist = request.POST.getlist('etiquetes', 0)

        #le añadimos los tags al objeto una vez salvado
        if type(etqlist) is list:
            if len(etqlist) > 0:
                #Los tags que ya estaban en DB
                for etiqueta in etqlist:
                    try:
                        objEtq = Etiqueta.objects.filter(pk=etiqueta,cela=cela).first()
                    except ValueError:
                        objEtq = None
                    #afegim la seguent comprovacio pq si l'etiqueta valia com a pk (...si era un numero) petaba
                    if not objEtq:
                    #creem etiqueta y la afegim al recurs
                        objEtq = Etiqueta.objects.create(nom= etiqueta,cela=cela)

                    rec.etiquetes.add(objEtq)


        # if len(etqAdd) > 0:
        #     etqAdd = str.split(etqAdd, ",")
        #     #Los tags que se tienen que añadir
        #     for etiqueta in etqAdd:
        #         objEtq, created = Etiqueta.objects.get_or_create(nom=etiqueta.strip(), cela=cela)
        #         rec.etiquetes.add(objEtq)


        notif_messages.add_message(request, notif_messages.INFO, "Has creat un nou recurs", 'success')

    return render(request, 'recurs/recurs_form.html',
                  {'formRecurs': formRecurs, 'request':request})


