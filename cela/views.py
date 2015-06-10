from .models import Cela, get_cela
from post.models import Post
from django.shortcuts import render, redirect, render_to_response
from django.views.generic.edit import CreateView, UpdateView
from .forms import celaForm
from django.http import HttpResponse
from usuari.models import UserProfile


def celaview(request,cela):
    request.session["cell"] = cela
    celax = Cela.objects.filter(pk=cela).first()
    if (celax.tipus == 'P'):
        extensVar = "base.html"
    else:
        extensVar = "baseRusc.html"

    if request.user.is_authenticated():
       if  UserProfile.objects.filter(user = request.user, cela=celax.pk).exists():
          return redirect('forum')

    return render(request,"cela.html", {'cela':celax,'extensVar':extensVar})


def peticioAcces(request):
    cela = get_cela(request)
    if not request.user.is_authenticated():
        return redirect('auth_login')

    perfilusuari, created =  UserProfile.objects.get_or_create(user=request.user, cela= cela,estat='E')

    return HttpResponse(" has solicitat acces.")


class celaCreateView(CreateView):
    model = Cela
    form_class = celaForm


class celaUpdateView(UpdateView):
    model = Cela
    form_class = celaForm
    template_name = "moderacio/cela_admin_form.html"


def moderacioPostView(request):
    ChekUsuariCellAdmin(request)

    cela = get_cela(request)
    posts = Post.objects.filter(moderacio='E', cela = cela)

    frm_modepost = request.POST.getlist('chk_post')
    acction =  request.POST.get('slc_modaction')
    if frm_modepost and acction:
        if acction == 'A':
            estatmod = 'A'
        else: estatmod = 'R'
        for post_pk in frm_modepost:
            Post.objects.filter(pk=post_pk).update(moderacio = estatmod)



    return render(request, "moderacio/mode_post.html", {'posts':posts, 'cela': cela})
def usuaris_cela(request):
    ChekUsuariCellAdmin(request)
    cela = get_cela(request)
    usuaris = UserProfile.objects.filter(cela=cela )

    frm_users = request.POST.getlist('chk_usuaris')
    acction =  request.POST.get('slc_modaction')
    if frm_users and acction:
        if acction == 'A':
            estatmod = 'A'
        elif acction == 'R':
            estatmod = 'R'
        elif acction == 'T':
            estatmod = 'T'

        for user in frm_users:
            UserProfile.objects.filter(pk=user, cela=cela).update(estat = estatmod)

    return render(request, "moderacio/membres_cela.html",{'usuaris':usuaris, 'cela':cela})



def acceptar_usuari(request):
    ChekUsuariCellAdmin(request)
    cela = get_cela(request)
    usuaris = UserProfile.objects.filter(cela=cela, estat = 'E' )

    frm_users = request.POST.getlist('chk_usuaris')
    acction =  request.POST.get('slc_modaction')
    if frm_users and acction:
        if acction == 'A':
            estatmod = 'A'
        else: estatmod = 'R'
        for user in frm_users:
            UserProfile.objects.filter(pk=user, cela=cela).update(estat = estatmod)

    return render(request, "moderacio/solicitud_ingres.html",{'usuaris':usuaris, 'cela':cela})

def ChekUsuariCellAdmin(request):
    cela = get_cela(request)
    if request.user.is_authenticated():
        up = UserProfile.objects.filter(user=request.user)
        if request.user in cela.moderadors.all():
            #todo que el redirect funcione, el resto todo OK
            return True
        else:
            return render_to_response( 'rusc.html' )





