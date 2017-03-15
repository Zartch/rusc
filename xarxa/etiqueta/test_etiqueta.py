# -*- coding: utf-8 -*-
from unittest import TestCase

from django.contrib.auth.models import User

from xarxa.etiqueta.models import Etiqueta, Tesauro
from cela.models import Cela


class TestEtiqueta(TestCase):

    def setUp(self):
        us= User.objects.filter(id=1).first()

        c1 = Cela.objects.filter(id=1).first()

        #Etiquetes Etiquetes
        tg1= Etiqueta.objects.create(nom='e1',descripcio= 'd1',usuari=us, tipologia = 'E',cela=c1)
        tg2= Etiqueta.objects.create(nom='e2',descripcio= 'd2',usuari=us, tipologia = 'E',cela=c1)
        tg3= Etiqueta.objects.create(nom='e3',descripcio= 'd3',usuari=us, tipologia = 'E',cela=c1)
        tg4= Etiqueta.objects.create(nom='e4',descripcio= 'd4',usuari=us, tipologia = 'E',cela=c1)

        #Etiquetes Moderació
        tgm1= Etiqueta.objects.create(nom='I+D',descripcio= 'recursos relacionados con el I+D',usuari=us, tipologia = 'M',cela=c1)
        tgm2= Etiqueta.objects.create(nom='Bibliografia',descripcio= 'recursos relacionados con la Bibliografia',usuari=us, tipologia = 'M',cela=c1)
        tgm3= Etiqueta.objects.create(nom='Informes',descripcio= 'recursos estadisticos, unicamente informes',usuari=us, tipologia = 'M',cela=c1)
        tgm4= Etiqueta.objects.create(nom='Experiencias',descripcio= 'Paginas de blog donde se habla de experiencias personales relacionadas',usuari=us, tipologia = 'M',cela=c1)


        #Ejemplo Tesauro Wikipedia
        ts1 = Etiqueta.objects.create(nom='Medios de transporte',usuari=us, tipologia = 'E',cela=c1)
        ts2 = Etiqueta.objects.create(nom='Medios de transporte terrestre',usuari=us, tipologia = 'E',cela=c1)
        ts3 = Etiqueta.objects.create(nom='Automóvil',usuari=us, tipologia = 'E',cela=c1)
        ts4 = Etiqueta.objects.create(nom='sedán',usuari=us, tipologia = 'E',cela=c1)
        ts5 = Etiqueta.objects.create(nom='coupé',usuari=us, tipologia = 'E',cela=c1)
        ts6 = Etiqueta.objects.create(nom='todo terreno',usuari=us, tipologia = 'E',cela=c1)
        ts7 = Etiqueta.objects.create(nom='Medios de transporte aéreo',usuari=us, tipologia = 'E',cela=c1)
        ts8 = Etiqueta.objects.create(nom='Medios de transporte marítimo',usuari=us, tipologia = 'E',cela=c1)


        Tesauro.objects.create(etq1=ts1,etq2=ts2,tipo='J')
        Tesauro.objects.create(etq1=ts2,etq2=ts3,tipo='J')

        Tesauro.objects.create(etq1=ts3,etq2=ts4,tipo='J')
        Tesauro.objects.create(etq1=ts3,etq2=ts5,tipo='J')
        Tesauro.objects.create(etq1=ts3,etq2=ts6,tipo='J')

        Tesauro.objects.create(etq1=ts1,etq2=ts7,tipo='J')
        Tesauro.objects.create(etq1=ts1,etq2=ts8,tipo='J')




