from django.shortcuts import render, get_object_or_404, redirect
from post.models import  Post
from etiqueta.models import Etiqueta
from cela.models import Cela, get_cela
from post.forms import postForm, VoteForm
from etiqueta.forms import etiquetaForm
from django.contrib.auth.models import User
from usuari.models import UserProfile
from django.contrib import messages as notif_messages
from django.forms.formsets import BaseFormSet
from django.forms.formsets import formset_factory
from recurs.forms import RecursForm
from recurs.models import Recurs
from notifications import notify

# Create your views here.
def forum(request):
    #ToDo https://docs.djangoproject.com/en/1.8/topics/http/middleware/
    cela= get_cela(request)
    #Filtrem els posts a aparèixer i utilitzem el manager pq afegeixi la columna on es dona el nºtotal de vots
    posts = Post.with_votes.get_queryset().filter(pare=None, cela = cela.pk).exclude(moderacio='R').filter(recurs=None)
    #Generem la queryset on es recullen tots els vots del passat i la tornem llistat de nombres
    #això ens serveix per saber si l'usuari ha votat abans o no al post en concret
    if not request.user.is_anonymous():
        voted = Vote.objects.filter(voter=request.user)
        voted = voted.values_list('post_id', flat=True)
    else:
        voted= []

    return render(request, "forum.html", {'posts': posts, 'cela': cela, 'voted':voted })

def postView(request, pkpost):
    # comentaris = Post.objects.filter(post = pkpost, pare = None)
    cela= get_cela(request)
    post = Post.with_votes.get_queryset().filter(pk=pkpost).exclude( moderacio='R').first()
    root = post.get_root_object()
    if not request.user.is_anonymous():
        voted = Vote.objects.filter(voter=request.user)
        voted = voted.values_list('post_id', flat=True)
    else:
        voted= []
    return render(request, "post.html", {'post': post, 'cela':cela,'voted':voted, 'root':root})


def postCreateView(request, pk=None):

    if not request.user.is_authenticated():
            return redirect('auth_login')

    cela= get_cela(request)
    perfilusuari, created =  UserProfile.objects.get_or_create(user=request.user, cela= cela)


    #Inicialitzem les variables
    titol = ""
    reply_root = []


    if pk:
        # Bloc per que prengui el titol de el comentari al que respón
        re = "Re:"
        reply = get_object_or_404(Post, pk=pk)
        titol = re + reply.titol        #Bloc per incloure les variables de Post al html per pintar el debat al que responem.
        reply_rootid = reply.get_root()
        reply_root = Post.objects.filter(pk=reply_rootid)

    formPost = postForm(request.POST or None, initial={'titol': titol})
    formEtiqueta = etiquetaForm(request.POST or None)
    RecursFormSet = formset_factory(RecursForm, formset=BaseFormSet)


    if formPost.is_valid():


        f = formPost.save(commit=False)

        #Recollim les variables per a crear les etiquetes o asociales al debat
        etqAdd = request.POST.get('etiquetes-autocomplete', 0)
        etqlist = request.POST.getlist('etiquetes', 0)

        # si responem a un comentari hem de afegir el pare
        if pk:
            comentari = get_object_or_404(Post, pk=pk)
            f.pare = comentari
            post = get_object_or_404(Post, pk=pk)
            f.post = post

        if not request.user.is_authenticated():
            return redirect('../../../../accounts/login')

        f.autor = request.user
        f.cela = cela

        f.save()

        notif_messages.add_message(request, notif_messages.INFO, "Has creat un nou post", 'success')

        #si el usuario no tiene un tipo de subscripción restrictrivo le añadimos:
        if (perfilusuari.tipusSubscripcio != 'X'):
            perfilusuari.subscriure(f.pk)



        #le añadimos los tags al objeto una vez salvado
        if type(etqlist) is list:
            #ToDo Comprobar si este if está de mas o es necesario
            if len(etqlist) > 0:
                #Los tags que ya estaban en DB
                for etiqueta in etqlist:
                    objEtq = Etiqueta.objects.filter(pk=etiqueta).first()
                    f.etiquetes.add(objEtq)

        if len(etqAdd) > 0:
            etqAdd = str.split(etqAdd, ",")
            #Los tags que se tienen que añadir
            for etiqueta in etqAdd:
                objEtq, created = Etiqueta.objects.get_or_create(nom=etiqueta.strip(), cela=cela)
                f.etiquetes.add(objEtq)


        #Affegim els recursos
        recurs_formset = RecursFormSet(request.POST)
        #numerador per poder recuperar el formset de les etiquetes a afegir
        numFormset = 0

        for recurs_form in recurs_formset:
            #nom del formset per a recuperar les etiqwuetes
            nomFormset = 'form-'+numFormset.__str__()+'-etiquetes-autocomplete'
            if recurs_form.is_valid():
                url = recurs_form.cleaned_data.get('url',False)
                descripcio = recurs_form.cleaned_data.get('descripcio',False)
                etqlistFormSet = recurs_form.cleaned_data.get('etiquetes',False)

                #Noves etiquetes o etiquetes sense haver fet correctament l'autocomplete
                etqAddFormSet =request.POST.get(nomFormset, 0)

                if url:
                    #treiem el espais per evitar duplicats
                    str.strip(url)
                    if descripcio:
                        str.strip(descripcio)

                    #Creem o obtenim el recurs que s'ha introduit en el post
                    rec, bool = Recurs.objects.get_or_create(cela = get_cela(request), descripcio=descripcio, url=url)

                    #Associem el recurs al post
                    f.recursos.add(rec)

                    #Si el recurs s'ha creat i encara no existia creem el post del recurs
                    # i l'associem al recurs per a saber quin post ha creat el recurs
                    if bool:
                        post_x = Post.objects.create(titol=rec.url, autor = request.user,  text="Discussio del recurs: "+ rec.descripcio, cela=get_cela(request))
                        rec.post_debat = post_x


                    #Creem o no el recurs, sempre volem afegir-li etiquetes al Recurs
                    #Associem les etiquetes del formset al recurs
                    for etq in etqlistFormSet:
                        rec.etiquetes.add(etq)

                    if len(etqAddFormSet) > 0:
                        etqPerCrear = etqAddFormSet.split(',')
                        #Los tags que se tienen que añadir
                        for etiqueta in etqPerCrear:
                            objEtq, created = Etiqueta.objects.get_or_create(nom=etiqueta.strip(), cela=cela)
                            rec.etiquetes.add(objEtq)

                    #Guardem els canvis a recurs
                    rec.save()
            #numerador per poder recuperar el formset de les etiquetes a afegir
            numFormset = numFormset +1


#Enviem les notificacions als usuaris subscrits
        if f.get_root() == f.pk:
            verbn = 'creat'
        else:
            verbn = 'respost'

        subscriptors = set()
        subscriptors.update(f.get_subscriptors())
        for usr in subscriptors:
            notify.send(f.autor, recipient= usr, verb=u''+verbn+'', action_object=f,
                 description=f.titol + " <br /> " + str(f.etiquetes.all()), target=f.cela)

            #Enviem el mail als subscrits, que tinguin activada la opció del mail
            up = UserProfile.objects.filter(user=usr, cela = f.cela).exclude(mailConf='N').first()
            #enviarMailPost(f,up.user.email)


        #Un cop hem creat o respós a un comentari, redirigim a la pagina del debat
        if not pk:
            returnpage = "/forum/post/" + str(f.pk)
        else:
            R = Recurs.objects.filter(post_debat = f.get_root())
            if R.count() > 0 :
                #Es un Debat de recurs, retornem a la pagina de recurs
                returnpage = '/recurs/'+ str(R.first().pk)
            else:
                #no es un debnat de recurs, retornem el debat
                returnpage = '/forum/post/' + str(reply_rootid)

            #Recurs.objects.filter(post_debat)



        return redirect(returnpage)

    #Variable per a coneixer fins a quin punt ha de pintar el debat, si no existeix vol dir que estém creant un debat nou.
    if pk == None:
        pk = 0


    return render(request, 'post/post_form.html',
                  {'id_pare': int(pk), 'reply_root': reply_root, 'formPost': formPost,
                   'formEtiqueta': formEtiqueta, 'cela':cela,'recurs_formset': RecursFormSet})




#enviament únic del mail a un usuari concret (notificacio mail)
from django.core.mail import send_mail
def enviarMailPost(post,user):
    #Todo Añadir las cabeceras a los mails para que los mails creen los arboles correctamente
    #Todo Modificar sistema para que se pueda responder desde el mail

    send_mail(post.titol, "DE: "+ str(post.autor) + " <br /> '\n' " +post.text, 'RUSC@example.com',  [user] , fail_silently=True)



#els seguents 3 objectes són cridats des de Ajax per a actualitzar la imatge de upvote/downvote

from django.http import HttpResponse
import json
from django.views.generic.edit import FormView
from post.models import Vote

class JSONFormMixin(object):
    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict), content_type='application/json')
        response.status = 200 if valid_form else 500
        return response



class VoteFormBaseView(FormView):
    form_class = VoteForm


    def create_response(self, vdict=dict(), valid_form=True):
        response = HttpResponse(json.dumps(vdict))
        response.status = 200 if valid_form else 500
        return response

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=form.data["post"])
        user = self.request.user
        prev_votes = Vote.objects.filter(voter=user, post=post)
        has_voted = (len(prev_votes) > 0)


        ret = {"success": 1}
        if not has_voted:
            # add vote
            v = Vote.objects.create(voter=user, post=post)
            ret["voteobj"] = v.id
        else:
            # delete vote
            prev_votes[0].delete()
            ret["unvoted"] = 1
        return self.create_response(ret, True)


    def form_invalid(self, form):
        ret = {"success": 0, "form_errors": form.errors }
        return self.create_response(ret, False)

class VoteFormView(JSONFormMixin, VoteFormBaseView):
    pass

def get_reel_etq(etq):
    return Post.objects.filter(etiquetes= etq)