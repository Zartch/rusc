__author__ = 'zartch'

from functools import partial, wraps

from django.shortcuts import render
from django.forms.formsets import formset_factory

from xarxa.etiqueta.models import Etiqueta
from cela.models import get_cela, TipoEtiqueta
from xarxa.ficha.models import Ficha, CamposFicha
from xarxa.ficha.forms import fichaForm

from django.db import transaction

def fichaListView(request):

    cela = get_cela(request)
    fichas = Ficha.objects.filter(cela = cela)

    return render(request, "llistatFichas.html",{'fichas': fichas})



def fichaCreateView(request):

    cela = get_cela(request)

    #Busquem les etiquetes que no tenen ficha
    # etq = Etiqueta.objects.filter(tipologia='M', cela = cela)
    fichas = Ficha.objects.filter(cela = cela)
    ambficha = []
    for ficha in fichas:
        ambficha.append(ficha)

    #restem per a mostrar les etiquetes que encara no tenen ficha
    # options = set(etq) - set(ambficha)

    fichas_formset = formset_factory(wraps(fichaForm)(partial(fichaForm, request=request)))

    if request.POST:
        with transaction.atomic():
            nom = request.POST.get('nom_ficha')
            f = Ficha.objects.create(cela=cela, nom=nom)


            numforms = int(request._post.get("form-TOTAL_FORMS"))
            while (numforms > 0):
                numforms -= 1
                descrip = request._post.get("form-"+str(numforms)+"-descrip")
                obliatorio = request._post.get("form-"+str(numforms)+"-obliatorio")
                hint = request._post.get("form-"+str(numforms)+"-hint")

                CamposFicha.objects.create(ficha = f, obliatorio=obliatorio, hint=hint, descrip=descrip)


        return render(request, "llistatFichas.html",{'fichas': fichas})
    return render(request, "novaFicha.html",{ 'fichas_formset':fichas_formset})

