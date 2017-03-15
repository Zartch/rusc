# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from notifications import notify
from django.contrib import messages as notif_messages
from django.core.urlresolvers import reverse
from django.contrib.auth.models import  User

from cela.forms import celaForm, celaModForm
from cela.models import get_cela, Cela, Tema
from xarxa.post.models import Post,folksonomia
from xarxa.etiqueta.models import Etiqueta, Tesauro, jsonSubdits
from xarxa.usuari.models import UserProfile


def ruscView(request):

    celas = Cela.objects.exclude(tipus='X')
    notif=[]
    if request.user.is_authenticated():
        notif = request.user.notifications.unread()

    return render(request, "rusc.html", {'celas':celas,'notifications': notif})

def celaview(request,cela):
    request.session["cell"] = cela
    celax = Cela.objects.filter(pk=cela).first()

    if (celax.tipus == 'P'):
        extensVar = "base.html"
    else:
        extensVar = "baseRusc.html"

    llistat_usuaris = UserProfile.objects.filter(cela = celax)
    llistat_etq = Etiqueta.objects.filter(cela=celax)
    llistat_temas = celax.temas.all()

    if request.user.is_authenticated():
        up =  UserProfile.objects.filter(user = request.user, cela=celax.pk)
        if  up.exists():
           if up.first().estat == 'A':
            return redirect('forum')

    #formulari per las preguntes de perfil personal obligatori
    infoRequired = []
    for dato in celax.personal.all():
        infoRequired.append(dato)

    return render(request, "cela.html", {'extensVar':extensVar, 'llistat_usuaris':llistat_usuaris, 'llistat_etq':llistat_etq,
                                         'infoRequired':infoRequired, 'llistat_temas':llistat_temas})

#la seguent funció serveix per a canviarli la cela on es troba l'usuari i redireccionarlo
#a la URL que se li hagi passat a la funció
def celachange(request,cela,url):
    request.session["cell"] = cela
    return redirect(url, request.user)

class celaCreateView(CreateView):
    model = Cela
    form_class = celaForm

    #Si creem una xarxa s'afegeixen moderadors, s'ha de crear el user profile, per a que el moderador no s'hagi d'acceptar a si mateix
    def get_success_url(self):
        mod = self.request.user
        #Afegim al usuari que ha creat la xarxa com a moderador
        self.object.moderadors.add(mod)
        #creem el userprofile de el moderador
        UserProfile.objects.get_or_create(user=mod, cela=self.object)

        #Enviem el mail amb la informació de la cela y el enllaç als documents:
        cuerpo = " Estás recibiendo este mail por que acabas de crear una red \n " \
                 " A partir de ahora la red : "+self.object.pregunta + " estará disponible en el siguiente enlace:\n" \
                 " m1l3.net/rusc/" + str(self.object.id) + "/\n"+\
                 " Los siguientes documentos, son muy importantes. Leetelos o el coco vendrá y te comerá\n"+ \
                 " Enlace al documento de '' http://m1l3.net/static/Docs/acceptacion/Doc.txt' \n"+ \
                 " Enlace al documento de '' http://m1l3.net/static/Docs/acceptacion/Doc.txt' \n"+ \
                 " Enlace al documento de '' http://m1l3.net/static/Docs/acceptacion/Doc.txt' \n"

        send_mail("Nueva red " + self.object.pregunta, cuerpo , "root@gmail.com", [self.request.user.email] )


        notif_messages.add_message(self.request, notif_messages.INFO, "Has creat una nova cela", 'success')
        return reverse('cela', args=[self.object.pk] )

    def form_invalid(self, form):
        notif_messages.add_message(self.request, notif_messages.INFO, "corregeix els errors indicats", 'warning')
        return super(celaCreateView, self).form_invalid(form)

    def form_valid(self, form):
        #hem de crear els temas abans de la creació del objecte

        temas = form.data.getlist("temas")
        for nom_tema in temas:
            Tema.objects.get_or_create(nom = nom_tema)

        return super(celaCreateView, self).form_valid(form)

class celaUpdateView(UpdateView):
    model = Cela
    form_class = celaModForm
    template_name = "cela/cela_form.html"
    #template_name = "moderacio/cela_admin_form.html"

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
    #data = {"name": "AUTOMÓVIL", "size": 3534, "children": [{"name": "Sedan", "size": 6714},{"name": "Todoterreno", "size": 743}]}
    data = {"name": get_cela(request).pregunta, "size": 200, "children":[]}

    #lista de etiquetas que forman parte de un tesauro jerarquico
    arbre = Tesauro.objects.filter(tipo='J')
    #selecionar els pares de tots
    #fem un llistat de id de etiquetes que son formen part de una relació jerarquica
    etqforts = {}
    etqdebil = {}
    for tes in arbre:
        etqforts[tes.etq1] = 0
        etqdebil[tes.etq2] = 0

    #restem la llista de debils als forts, per obtenir aquells que mai han sigut debils
    #hi son a les 2 llistas:?
    #pares={ k:int(etqforts[k]) - int(etqdebil[k]) for k in etqdebil if k in etqdebil }
    pares = set(etqforts) - set(etqdebil)
    for etq in pares:
        childs = data['children']
        nens = jsonSubdits(etq)
        childs.append(nens)
        data['children'] = childs


    return JsonResponse(dict(data), safe=False)

def tesauro_jerarquic(request):
    return render(request, "visual/tesauro_jerarquic.html", {})

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
    return render(request, "visual/network.html", {'etq':etq, 'reel': reel, 'posts':posts, 'd':d} )

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


    return render(request, "visual/PostRelacions.html", {'data':data} )

def visual(request):

    chk_folk =  request.POST.get('chk_folk')
    cela = get_cela(request)
    etqs = Etiqueta.objects.filter(cela=cela)
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
        s['cela']= cela.slug
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

    return render(request, "visual/visual.html", {'data':data} )

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


        for etq in Etiqueta.objects.filter(cela = cela):
            d.append(etq.slug)
        if len(d) > 0:
            s['musicians'] = d.copy()
        else:
            s['musicians'] = []
        data.append(s.copy())


    return render(request, "visual/CelaRelacions.html", {'data':data} )