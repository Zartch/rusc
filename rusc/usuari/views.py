# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic.edit import UpdateView
from django.contrib import messages as notif_messages

from rusc.usuari.models import UserProfile, UserInfo
from rusc.usuari.forms import userProfileGeneralForm, userProfileForm
from cela.models import get_cela
from rusc.post.models import Post, Vote
from rusc.etiqueta.models import Etiqueta
from django.forms.formsets import BaseFormSet
from django.forms.formsets import formset_factory
from rusc.usuari.forms import userInfoForm

#vista peer mostrar els post en estat de moderacio del usuari
def moderacioPostView(request):
    cela = get_cela(request)
    post_entramit = Post.objects.filter(autor=request.user,moderacio ='E', cela=cela)
    post_rebutjats = Post.objects.filter(autor=request.user,moderacio ='R', cela=cela)

    return render(request, 'moderacioPost.html', {'post_entramit':post_entramit, 'post_rebutjats':post_rebutjats})

def perfilview(request):

    if not request.user.is_authenticated():
        return redirect('auth_login')

    perfilusuari = UserProfile.objects.filter(user=request.user.pk).first()
    form_user = userProfileGeneralForm(request.POST or None)
    up= UserProfile.objects.filter(user=request.user)

    if form_user.is_valid():
        f = form_user.save(commit=False)
        UserProfile.objects.filter(user=request.user).update(tipusSubscripcio=f.tipusSubscripcio,mailConf= f.mailConf )
        notif_messages.add_message(request, notif_messages.INFO, "Configuració personal actualitzada a totes les celes", 'success')
        return redirect('rusc', )


    return render(request, 'perfil_usuari.html', {'form_user':form_user, 'up':up})

def viewuser(request,pk):
    if not request.user.is_authenticated():
        return redirect('auth_login')

    perfilusuari = UserProfile.objects.filter(pk=pk).first()
    usuari = User.objects.filter(pk=perfilusuari.user.pk).first()

    return render(request, 'perfil_usuari.html', {'usuari': usuari})

from itertools import chain
def viewuserprofile(request,pk):
    cela = get_cela(request)
    if not request.user.is_authenticated():
        return redirect('auth_login')

    profile = UserProfile.objects.filter(pk=pk, cela=get_cela(request)).first()
    usuari = profile.user
    userInfo = UserInfo.objects.filter(usr = profile).exclude(visible = False)

    posts_publicats = Post.objects.filter(autor=usuari, pare = None, cela = cela)
    respostes_publicades = Post.objects.filter(autor=usuari, cela = cela).exclude(pare = None)
    etiquetes1 = Etiqueta.objects.filter(post= posts_publicats)
    etiquetes2 = Etiqueta.objects.filter(post= respostes_publicades)

    etiquetes = list(chain(etiquetes2, etiquetes1))

    voted = Vote.objects.filter(voter=request.user)
    voted = voted.values_list('post_id', flat=True)

    #info_formset =  formset_factory(userInfoForm, formset= BaseFormSet)
    from functools import partial, wraps
    info_formset = formset_factory(wraps(userInfoForm)(partial(userInfoForm, request=request)))
    #'antig':usuari.date_joined,
    return render(request, 'perfil_view.html', {'usuari': usuari, 'nMiss': posts_publicats.count(), 'nRes':respostes_publicades.count(),'userInfo':userInfo,
                                                'posts':posts_publicats,'etiquetes':etiquetes, 'profile': profile, 'voted':voted, 'info_formset':info_formset })

class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = userProfileForm
    template_name = "userProfile_form.html"


    def get_object(self, queryset=None):
       queryset = UserProfile.objects.filter(user=self.request.user, cela= get_cela(self.request)).first()
       return queryset

    def get_context_data(self, **kwargs):
        from django.forms.models import modelformset_factory
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        cela =  get_cela(self.request)
        context['cela'] = cela
        from functools import partial, wraps

        up = UserProfile.objects.get(user = self.request.user, cela = cela)
        ui = UserInfo.objects.filter(usr = up)
        info = []
        extra = 0
        #Creamos un array para poner nuestros initial values
        #Todo Mejorar esta guarrada
        for userinfo in ui:
            #Lo hacemos 2 veces por que hará 2 pops (esto es muy guarro pero 'funciona')
            info.append([userinfo.etq.pk, userinfo.visible])
            #info.append(userinfo.etq.pk)
            extra += 1
        #tenemos que iniciar almenos un form para poder añadir etiquetas de perfil
        if extra == 0:
            extra = 1

        info_formset = formset_factory(wraps(userInfoForm)(partial(userInfoForm, request=self.request, selected = info)),extra= extra)

        #inf_for =info_formset(initial = [{'etq':'cadena','visible':False},{'etq': 'otra','visible':True}])
        #RelatedFormset = modelformset_factory(UserInfo, userInfoForm, extra=1)
        #up = UserProfile.objects.get(user = self.request.user, cela = get_cela(self.request))
        #formset = RelatedFormset(queryset=UserInfo.objects.filter(usr= up))

        context['info_formset'] = info_formset
        return context

    def form_valid(self, form):
        from rusc.usuari.models import UserInfo

        cela = get_cela(self.request)
        numforms = int(form.data.get("form-TOTAL_FORMS"))

        #Obtenim el userprofile de la cela concreta
        usr = UserProfile.objects.get(cela = cela, user = self.request.user)
        #Eliminem les etiquetes per tornales a crear de nou amb el visible correctament
        UserInfo.objects.filter(usr = usr).delete()

        #iterem per cada un dels formularis
        while (numforms > 0):
            numforms -= 1
            etq = form.data.get("form-"+str(numforms)+"-etq")
            visible = form.data.get("form-"+str(numforms)+"-visible")
            #Nuestra etiqueta puede estar vacia.
            if etq != '':
                #Buscas la etiqueta como ID, si no está la creas como nombre etiqueta
                try:
                    e = Etiqueta.objects.get(id = etq)
                except:
                    e = Etiqueta.objects.create(nom = etq,moderacio='E', cela = cela )
                #El chek devuelve  on o nada
                if visible == 'on':
                    visible = True
                else:
                    visible = False
                # afegim la relació amb les etiquetes de perfil
                inf, created = UserInfo.objects.get_or_create(etq = e, usr = usr, visible = visible)

        notif_messages.add_message(self.request, notif_messages.INFO, "Usuari modificat correctament", 'success')
        return super(UserProfileUpdateView, self).form_valid(form)

    def form_invalid(self, form):
        notif_messages.add_message(self.request, notif_messages.INFO, "corregeix els errors indicats", 'warning')
        return super(UserProfileUpdateView, self).form_invalid(form)


#Probes per el m2mSelector, funciona
from django.forms import ModelForm

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'user_permissions')

def index(request):
    u = User.objects.get(pk=1)
    return render(request, 'm2mselector.html', {'form': UserForm(instance=u)})