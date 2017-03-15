# -*- coding: utf-8 -*-
from datetime import datetime

from django.shortcuts import render

from cela.models import get_cela, TipoEtiqueta
from xarxa.etiqueta.models import Etiqueta
from xarxa.usuari.models import UserProfile
from xarxa.post.models import Post
from xarxa.recurs.models import Recurs


def view_resums(request):
    tipo, created = TipoEtiqueta.objects.get_or_create(primary = 'S')
    etqResum = Etiqueta.objects.get_or_create(nom='Resum', tipologia = tipo, cela= get_cela(request) )
    resums = Post.objects.filter(etiquetes__nom = 'Resum')

    return render(request, "forum.html", {'posts':resums})

def resumCreateView(request):
    #etiquetas para flitrar
    #un rango de fechas
    #Usuarios concretos o todos
    cela = get_cela(request)
    etqs = Etiqueta.objects.filter(cela=cela)
    users = UserProfile.objects.filter(cela=cela)

    etiquetas = []
    for etq in etqs:
        etiquetas.append({'id':etq.pk, 'text':etq.nom })
    usuaris = []
    for user in users:
        usuaris.append({'id':user.pk, 'text':user.user.username  + " " + user.user.first_name + " " })


    if request.POST or False:
        etq = request.POST.get('sel_etqs') or []
        usr = request.POST.get('sel_users')or []
        dtTo = request.POST.get('dtTo')or None
        dtfrom = request.POST.get('dtfrom')or None
        borrador = "Esto es un borrador"

        #Si la fecha desde no existe tomamos la fecha de creación de la cela
        if not dtfrom:
            dtfrom = cela.datacreacio
        #si la fecha hasta no existe tomamos hoy
        if not dtTo:
            dtTo = datetime.today()

        recursos = []
        recursos_str=""
        for e in etq:
            qs = Recurs.objects.filter(etiquetes=e, datahora__range=(dtfrom,dtTo))
            for r in qs:
                recursos_str += " http://51.254.96.92:8000/recurs/"+str(r.pk) + "  " + str(r) + " \n"
            recursos.append(qs)
        for u in usr:
            qs = Recurs.objects.filter(post_debat__autor=u, datahora__range=(dtfrom,dtTo))
            for r in qs:
                recursos_str += " http://51.254.96.92:8000/recurs/"+str(r.pk)+ "  " + str(r) + " \n"
            recursos.append(qs)
        list(set(recursos))
        
        #created_at__range=(start_date, end_date)
        posts = []
        posts_str = ""
        for e in etq:
            qs = Post.objects.filter(etiquetes=e, datahora__range=(dtfrom,dtTo))
            for p in qs:
                posts_str += " http://51.254.96.92:8000/forum/post/" + str(p.pk)+ "  " + str(p) + " \n"
            posts.append(qs)
        for u in usr:
            qs = Post.objects.filter(autor=u, datahora__range=(dtfrom,dtTo))
            for p in qs:
                posts_str += " http://51.254.96.92:8000/forum/post/" + str(p.pk)+ "  " + str(p) + " \n"
            posts.append(qs)
        list(set(posts))

        #relaciones entre usuarios
        usuaris = []
        #dado un recurso, todos los usuarios que han participado en su discusión
        #Dado un hilo, todos los usuarios que han participado en su deiscusión
        #relaciones entre hilos
        borrador =  "Parametros usados: "+ "\n" \
                  + "Etiquetas: "+ str(etq)+ "\n" \
                  + "Usuarios: "+str(usr)+ "\n" \
                  + "posts: \n " + posts_str + "\n" \
                  + "recuros: \n"+ recursos_str

        return  render(request, 'new_resum.html', {'cela':cela,'etqs':etiquetas, 'users': usuaris, 'borrador':borrador})

    return render(request, 'new_resum.html', {'cela':cela,'etqs':etiquetas, 'users': usuaris})
