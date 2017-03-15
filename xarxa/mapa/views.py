__author__ = 'zartch'
from cela.models import get_cela
from xarxa.etiqueta.models import Etiqueta


def mapa_cela(request):
    cela= get_cela(request)

    zonas = Etiqueta.objects