__author__ = 'zartch'

from functools import partial, wraps

from django.shortcuts import render
from django.forms.formsets import formset_factory

from xarxa.etiqueta.models import Etiqueta
from cela.models import get_cela, TipoEtiqueta
from xarxa.etiqueta.models import Ficha
from xarxa.ficha.forms import fichaForm


def fichaListView(request):

    cela = get_cela(request)
    fichas = Ficha.objects.filter(etq__cela = cela)

    return render(request, "llistatFichas.html",{'fichas': fichas})



def fichaCreateView(request):

    cela = get_cela(request)

    #Busquem les etiquetes que no tenen ficha
    etq = Etiqueta.objects.filter(tipologia='M', cela = cela)
    fichas = Ficha.objects.filter(etq__cela = cela)
    ambficha = []
    for ficha in fichas:
        ambficha.append(ficha.etq)

    #restem per a mostrar les etiquetes que encara no tenen ficha
    options = set(etq) - set(ambficha)

    fichas_formset = formset_factory(wraps(fichaForm)(partial(fichaForm, request=request)))

    if request.POST or None:
        etiqueta = Etiqueta.objects.get(pk = request._post.get("ddl_ficha"))
        numforms = int(request._post.get("form-TOTAL_FORMS"))
        while (numforms > 0):
            numforms -= 1
            idtipo = request._post.get("form-"+str(numforms)+"-tipo")
            tipo = TipoEtiqueta.objects.get(pk= idtipo)
            descrip = request._post.get("form-"+str(numforms)+"-descrip")
            obliatorio = request._post.get("form-"+str(numforms)+"-obliatorio")
            hint = request._post.get("form-"+str(numforms)+"-hint")

            Ficha.objects.create(etq=etiqueta, tipo = tipo, descrip = descrip,
                                  obliatorio = obliatorio, hint = hint)

        return render(request, "llistatFichas.html",{'fichas': fichas})
    return render(request, "novaFicha.html",{'options': options, 'fichas_formset':fichas_formset})

