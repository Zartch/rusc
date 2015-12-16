# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages as notif_messages
from notifications import notify

from cela.models import get_cela
from rusc.post.models import Post
from rusc.usuari.models import UserProfile


#Vista per acceptar o rebutjar post, en cas de acceptació tornem a la mateixa pagina
#En cas de negació enviém un missatge al usuari per tal de donar la explicació de per que rebutjem el post
def acceptarRebutjarPost(request,pkpost, action):
    cela = get_cela(request)
    posts = Post.objects.filter(cela = cela).exclude(moderacio='A').exclude(moderacio='R')

    post = Post.objects.get(pk=pkpost)

    verb = 'Error'
    descripcio= ""
    if action == 'cancel':
        text_rebutg =  request.POST.get('text') or None
        user = request.user
        if text_rebutg:
            post.missModeracio.create(author = user, body = text_rebutg)
            post.moderacio = 'R'
            verb = 'Rebutjat'
            descripcio = text_rebutg
        else:
            notif_messages.add_message(request, notif_messages.warning, "S'ha de indicar una raò per el rebutg del post", 'error')
    elif action == 'OK':
        post.moderacio = 'A'
        verb = 'acteptat'
        descripcio = post.text

    #El usuari ha de rebre una notificació quan un missatge es creat al debat de moderació de un post
    notify.send(request.user, recipient= post.autor, verb=u' '+verb+' ', action_object= post ,
             description=  descripcio , target = post.cela)

    post.save()
    notif_messages.add_message(request, notif_messages.INFO, "Moderació realitzada", 'success')
    return render(request, "moderacio/mode_post.html", {'posts':posts} )

def peticioAcces(request):
    cela = get_cela(request)
    if not request.user.is_authenticated():
        return redirect('auth_login')
    else:
        perfilusuari, created = UserProfile.objects.get_or_create(user=request.user,cela= cela)
        if created:
            perfilusuari.estat = 'E'
            perfilusuari.save()
    return HttpResponse(" has solicitat acces.")


def moderacioPostView(request):

    ChekUsuariCellAdmin(request)
    cela = get_cela(request)
    posts = Post.objects.filter(cela = cela).exclude(moderacio='A').exclude(moderacio='R')

    #Recollim els checkbboxes dels post
    frm_modepost = request.POST.getlist('chk_post')
    #Recollim la acció a realizar
    acction =  request.POST.get('slc_modaction')
    if frm_modepost and acction:
        #només aceptem la acció 'A'(acceptar), o 'R'(rebutjar)
        if acction == 'A':
            estatmod = 'A'
        else: estatmod = 'R'
        #updatejem el estat de moderacio dels post
        for post_pk in frm_modepost:
            Post.objects.filter(pk=post_pk).update(moderacio = estatmod)
        notif_messages.add_message(request, notif_messages.INFO, "Moderació realitzada" , 'success')

    return render(request, "moderacio/mode_post.html", {'posts':posts})

#vista per a que el moderador modifiqui usuaris ja creats i aprovats previament
def usuaris_cela(request):

    ChekUsuariCellAdmin(request)
    cela = get_cela(request)
    usuaris = UserProfile.objects.filter(cela=cela)

    frm_users = request.POST.getlist('chk_usuaris')
    acction =  request.POST.get('slc_modaction')
    missatge= "Usuaris "
    if frm_users and acction:
        if acction == 'A':
            estatmod = 'A'
            missatge= missatge + " acceptats"
        elif acction == 'R':
            estatmod = 'R'
            missatge= missatge + " rebutjats"
        elif acction == 'T':
            estatmod = 'T'
            missatge= missatge + " marcats com troll"

        for user in frm_users:
            UserProfile.objects.filter(pk=user, cela=cela).update(estat = estatmod)

        notif_messages.add_message(request, notif_messages.INFO, missatge , 'success')

    return render(request, "moderacio/membres_cela.html",{'usuaris':usuaris})

#funció que comprova que el usuari loguejat sigui admin de la cela on es troba
def ChekUsuariCellAdmin(request):
    cela = get_cela(request)
    if request.user.is_authenticated():
        up = UserProfile.objects.filter(user=request.user)
        if request.user in cela.moderadors.all():
            return True
        else:
            notif_messages.add_message(request, notif_messages.INFO, "Te estamos observando espabilao" , 'success')
            return redirect( 'forum' )

#vista per a que el moderador accepti o rebutji nous ingressos d'usuari
def acceptar_usuari(request):
    ChekUsuariCellAdmin(request)
    cela = get_cela(request)
    usuaris = UserProfile.objects.filter(cela=cela, estat = 'E' )

    frm_users = request.POST.getlist('chk_usuaris')
    acction =  request.POST.get('slc_modaction')

    missatge= "Usuaris "
    if frm_users and acction:
        if acction == 'A':
            estatmod = 'A'
            missatge= missatge + " acceptats"
        else:
            estatmod = 'R'
            missatge= missatge + " rebutjats"
        for user in frm_users:
            UserProfile.objects.filter(pk=user, cela=cela).update(estat = estatmod)

        notif_messages.add_message(request, notif_messages.INFO, missatge , 'success')

    return render(request, "moderacio/solicitud_ingres.html",{'usuaris':usuaris})

from django_messages.models import Message
def missatge_cela(request):

    if request.POST:
        usuaris = UserProfile.objects.filter(cela= get_cela(request))
        for user in usuaris:
            Message.objects.create(subject=request.POST['asumpte'], body=request.POST['text'],
                                   sender= request.user, recipient= user.user)
        notif_messages.add_message(request, notif_messages.INFO, "Enviats Missatges a tota la xarxa", 'success')

    return render(request, "moderacio/missatgeriaCela.html", {} )