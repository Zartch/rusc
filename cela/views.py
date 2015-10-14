# -*- coding: utf-8 -*-
from .models import Cela, get_cela
from post.models import Post,folksonomia
from etiqueta.models import Etiqueta, Tesauro
from django.shortcuts import render, redirect, render_to_response
from django.views.generic.edit import CreateView, UpdateView
from .forms import celaForm
from django.http import HttpResponse
from usuari.models import UserProfile
from django.contrib.auth.models import User
from notifications import notify
from django.contrib import messages as notif_messages
from django.core.urlresolvers import reverse
import json

def celaview(request,cela):
    request.session["cell"] = cela
    celax = Cela.objects.filter(pk=cela).first()
    if (celax.tipus == 'P'):
        extensVar = "base.html"
    else:
        extensVar = "baseRusc.html"

    llistat_usuaris = UserProfile.objects.filter(cela = celax)
    llistat_etq = Etiqueta.objects.filter(cela=celax)


    if request.user.is_authenticated():
       if  UserProfile.objects.filter(user = request.user, cela=celax.pk).exists():
          return redirect('forum')

    return render(request,"cela.html", {'extensVar':extensVar, 'llistat_usuaris':llistat_usuaris, 'llistat_etq':llistat_etq})

#la seguent funció serveix per a canviarli la cela on es troba l'usuari i redireccionarlo
#a la URL que se li hagi passat a la funció
def celachange(request,cela,url):
    request.session["cell"] = cela
    return redirect(url, request.user)

def peticioAcces(request):
    cela = get_cela(request)
    if not request.user.is_authenticated():
        return redirect('auth_login')

    perfilusuari, created =  UserProfile.objects.get_or_create(user=request.user,estat='E')

    return HttpResponse(" has solicitat acces.")


class celaCreateView(CreateView):
    model = Cela
    form_class = celaForm

    #Si creem una xarxa s'afegeixen moderadors, s'ha de crear el user profile, per a que el moderador no s'hagi d'acceptar a si mateix
    def get_success_url(self):
        for mod in self.object.moderadors.all():
            UserProfile.objects.get_or_create(user=mod, cela=self.object)
        notif_messages.add_message(self.request, notif_messages.INFO, "Has creat una nova cela", 'success')
        return reverse('cela', args=[self.object.pk] )

    def form_invalid(self, form):
        notif_messages.add_message(self.request, notif_messages.INFO, "corregeix els errors indicats", 'warning')
        return super(celaCreateView, self).form_invalid(form)


class celaUpdateView(UpdateView):
    model = Cela
    form_class = celaForm
    template_name = "moderacio/cela_admin_form.html"

    def form_valid(self, form):
        notif_messages.add_message(self.request, notif_messages.INFO, "Has modificat una cela", 'success')
        return super(celaUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        notif_messages.add_message(self.request, notif_messages.INFO, "corregeix els errors indicats", 'warning')
        return super(celaUpdateView, self).form_invalid(form)

    #Si afegim moderadors, hem de crear el user profile, per a que el moderador no s'hagi d'acceptar a si mateix
    def get_success_url(self):
        for mod in self.object.moderadors.all():
            UserProfile.objects.get_or_create(user=mod, cela=self.object)
        notif_messages.add_message(self.request, notif_messages.INFO, "Cela modificada correctament", 'success')
        return reverse('cela', args=[self.object.pk] )

def moderacioPostView(request):

    ChekUsuariCellAdmin(request)
    cela = get_cela(request)
    posts = Post.objects.filter(moderacio='E', cela = cela)

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
    usuaris = UserProfile.objects.filter(cela=cela )

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


#vista per a convidar usuaris a la cela
def cela_convidar(request):
    cela = get_cela(request)

    usuaris_to_add= []
    missusu = False

    if request.POST.get('mails'):
        frm_invmails= str(request.POST.get('mails')).split(",")
        #convidar via mail (Send Mail)
        for mail in frm_invmails:
            mail = mail.strip()
            #comprobem que els mails no estiguin donats de alta a la xarxa
            alta = User.objects.filter(email = mail).first()
            if not alta:
                if validateEmail(mail):
                    UserProfile.objects.create(cela=cela, estat='E', email_p=mail)
                    enviarInvitacio(mail,cela)
                    missusu = True
            else:
                usuaris_to_add.append(alta)


    if (request.POST.get('usuaris') or len(usuaris_to_add) > 0 ):
        frm_invusers = str(request.POST.get('usuaris')).split(",")
        frm_invusers.extend(usuaris_to_add)
        #convididar usuaris (+UserProfile A) + notification
        for username in frm_invusers:
            username = str(username).strip()
            u = User.objects.filter(username= username).first()
            if u:
                UserProfile.objects.get_or_create(user=u,cela=cela, estat='E')
                notify.send(request.user, recipient= u, verb=u'convidat a la cela', action_object=cela,
                     description=cela.descripcio + " ", target=cela)
                missusu = True

    if missusu:
        notif_messages.add_message(request, notif_messages.INFO, "Usuaris convidats" , 'success')



    if isinstance(cela, Cela) and request.user.is_authenticated():
        #el seguent llistat d'usuaris es d'us exclusiu per a l'autocomplete
        usuaris = User.objects.all().exclude(userprofile__cela = cela)
        usuaris_list = []
        for usu in usuaris:
            usuaris_list.append(usu.username)

        return render(request, "convidar.html",{'usuaris':usuaris_list})


from django.core.mail import send_mail

#funció exclusivament per a enviar invitacio a cela a un usuari que se li passa a la funció
def enviarInvitacio(user,cela):

    send_mail("Convidat a RUSC", "T'han convidat a la xarxa "+ cela.pregunta+ "http://127.0.0.1:8000/accounts/register/", 'RUSC@example.com',  [user] , fail_silently=True )



#en cas de que si estigui, enviar invitació al usuari
def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError

    try:
        validate_email( email )
        return True
    except ValidationError:
        return False


from django.http import JsonResponse
def tesauro_jerarquic_json(request):
    data = {"name": "AUTOMÓVIL", "size": 3534, "children": [{"name": "Sedan", "size": 6714},{"name": "Todoterreno", "size": 743}]}

    return JsonResponse(dict(data), safe=False)

def tesauro_jerarquic(request):
    return render(request,"visual/tesauro_jerarquic.html", {})

def network(request):

    etq = Etiqueta.objects.values_list('nom', flat=True).filter(cela=get_cela(request))
    reel = Tesauro.objects.values_list('etq1__nom','etq2__nom').filter(etq1__cela=get_cela(request))
    posts = Post.objects.values_list('titol', flat=True).filter(cela=get_cela(request))
    post_list = Post.objects.filter(cela=get_cela(request))

    d = []
    for pt in post_list:
        x = pt.titol
        r = list(pt.etiquetes.values_list('nom', flat=True))
        d.append((x,r))


    reel = list(reel)
    return render(request,"visual/network.html", {'etq':etq, 'reel': reel, 'posts':posts, 'd':d} )


def visualPost(request):

    posts = Post.objects.filter(cela=get_cela(request))
    s = {'artist':"",'title':"",'itunes':"",'cover':"",'color':"",'text':"",'musicians':[]}
    d=[]
    data = []

    for post in posts:
        s.clear()
        s['artist']= str(post.autor)
        s['title']= post.titol
        s['color']= "#47738C"
        s['text']= "#0A0606"
        d.clear()
        for etq in post.etiquetes.values_list('nom',flat=True):
            d.append(etq)
        if len(d) > 0:
            s['musicians'] = d.copy()
        else:
            s['musicians'] = []
        data.append(s.copy())


    return render(request,"visual/PostRelacions.html", {'data':data} )


def visual(request):

    chk_folk =  request.POST.get('chk_folk')

    etqs = Etiqueta.objects.filter(cela=get_cela(request))
    data = []
    s = {'artist':"",'title':"",'itunes':"",'cover':"",'color':"",'text':"",'musicians':[]}
    d=[]
    for etq in etqs:
        s.clear()
        s['artist']= etq.nom
        s['title']= etq.nom
        s['itunes']= "www.itunes.com"
        s['cover']= "Cover"
        s['color']= "#47738C"
        s['text']= "#0A0606"
        d.clear()

        #taxonomia
        for t in etq.relacio.values_list('nom', flat=True):
            d.append(t)
        for reel in Tesauro.objects.filter(etq2=etq):
            d.append(reel.etq1.nom)
        d = list(set(d))

        if chk_folk:
            #folksonomia
            posts = Post.objects.filter(etiquetes= etq)
            llist = folksonomia(posts)
            for etq,num in llist.items():
                d.append(etq)
            d = list(set(d))

        if len(d) > 0:
            s['musicians'] = d.copy()
        else:
            s['musicians'] = []

        data.append(s.copy())

    return render(request,"visual/visual.html", {'data':data} )


from django_messages.models import Message
def missatge_cela(request):

    if request.POST:
        usuaris = UserProfile.objects.filter(cela= get_cela(request))
        for user in usuaris:
            Message.objects.create(subject=request.POST['asumpte'], body=request.POST['text'],
                                   sender= request.user, recipient= user.user)
        notif_messages.add_message(request, notif_messages.INFO, "Enviats Missatges a tota la xarxa", 'success')

    return render(request,"moderacio/missatgeriaCela.html", {} )



def VisualCelas(request):

    celas = Cela.objects.filter(tipus='P')
    s = {'artist':"",'title':"",'itunes':"",'cover':"",'color':"",'text':"",'musicians':[]}
    d=[]
    data = []

    for cela in celas:
        s.clear()
        s['artist']= str(cela.descripcio)
        s['title']= cela.slug
        s['color']= "#47738C"
        s['text']= "#0A0606"
        s['pk'] = cela.pk
        d.clear()


        for etq in cela.get_etiquetes():
            d.append(etq.slug)
        if len(d) > 0:
            s['musicians'] = d.copy()
        else:
            s['musicians'] = []
        data.append(s.copy())


    return render(request,"visual/CelaRelacions.html", {'data':data} )