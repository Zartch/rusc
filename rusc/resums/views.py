__author__ = 'zartch'
from django.shortcuts import render
from cela.models import get_cela
from rusc.etiqueta.models import Etiqueta
from rusc.usuari.models import UserProfile
from rusc.post.models import Post
from rusc.recurs.models import Recurs
from datetime import datetime

def view_resums(request):
    etqResum = Etiqueta.objects.get_or_create(nom='Resum', tipologia= 'S', cela= get_cela(request) )
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
        for e in etq:
            recursos.append(Recurs.objects.filter(etiquetes=e, datahora__range=(dtfrom,dtTo)))
        for u in usr:
            recursos.append(Recurs.objects.filter(post_debat__autor=u, datahora__range=(dtfrom,dtTo)))
        list(set(recursos))
        
        #created_at__range=(start_date, end_date)
        posts = []
        for e in etq:
            qs = Post.objects.filter(etiquetes=e, datahora__range=(dtfrom,dtTo))
            posts.append(qs)
        for u in usr:
            posts.append(Post.objects.filter(autor=u, datahora__range=(dtfrom,dtTo)))
        list(set(posts))

        #relaciones entre usuarios
        usuaris = []
        #dado un recurso, todos los usuarios que han participado en su discusión
        #Dado un hilo, todos los usuarios que han participado en su deiscusión
        #relaciones entre hilos

        borrador =  "Parametros usados: "+ "\n" \
                  + "Etiquetas: "+ str(etq)+ "\n" \
                  + "Usuarios: "+str(usr)+ "\n" \
                  + "posts: \n " + str(posts) + "\n" \
                  + "recuros: \n"+ str(recursos)

        return  render(request, 'new_resum.html', {'cela':cela,'etqs':etiquetas, 'users': usuaris, 'borrador':borrador})

    return render(request, 'new_resum.html', {'cela':cela,'etqs':etiquetas, 'users': usuaris})
