__author__ = 'Zartch'
from usuari.models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404



def perfilview(request):
    if request.user.is_authenticated():
        userpk = request.user.pk
    else:
        return redirect('auth_login')
    usuari = request.user
    perfilusuari = UserProfile.objects.filter(user=userpk).first()
    return render(request, 'perfil_usuari.html', {'usuari': usuari, 'perfilusuari':perfilusuari})


def viewuser(request,pk):
    if not request.user.is_authenticated():
        return redirect('auth_login')
    perfilusuari = UserProfile.objects.filter(pk=pk).first()
    usuari = User.objects.filter(pk=perfilusuari.user.pk).first()
    return render(request, 'perfil_usuari.html', {'usuari': usuari, 'perfilusuari':perfilusuari})

