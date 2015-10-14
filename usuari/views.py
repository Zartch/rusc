# -*- coding: utf-8 -*-
from usuari.models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.views.generic.edit import UpdateView
from usuari.forms import userProfileGeneralForm, userProfileForm
from cela.models import get_cela
from django.contrib import messages as notif_messages
from post.models import Post
from etiqueta.models import Etiqueta

from datetime import date, datetime, timedelta

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
    if not request.user.is_authenticated():
        return redirect('auth_login')

    usuari = User.objects.filter(pk=pk).first()
    profile = UserProfile.objects.filter(user__pk=pk, cela=get_cela(request)).first()

    posts_publicats = Post.objects.filter(autor=usuari, pare = None)
    respostes_publicades = Post.objects.filter(autor=usuari).exclude(pare = None)
    etiquetes1 = Etiqueta.objects.filter(post= posts_publicats)
    etiquetes2 = Etiqueta.objects.filter(post= respostes_publicades)

    etiquetes = list(chain(etiquetes2, etiquetes1))

    return render(request, 'perfil_view.html', {'usuari': usuari, 'nMiss': posts_publicats.count(), 'nRes':respostes_publicades.count(), 'antig':usuari.date_joined,
                                                'posts_publicats':posts_publicats,'etiquetes':etiquetes, 'profile': profile})

class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = userProfileForm
    template_name = "userProfile_form.html"

    def get_object(self, queryset=None):
       queryset = UserProfile.objects.filter(user=self.request.user, cela= get_cela(self.request)).first()
       return queryset

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        context['cela'] = get_cela(self.request)
        return context

    def form_valid(self, form):
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