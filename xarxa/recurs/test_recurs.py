# -*- coding: utf-8 -*-
from unittest import TestCase

from django.contrib.auth.models import User

from xarxa.etiqueta.models import Etiqueta
from xarxa.recurs.models import Recurs


class TestRecurs(TestCase):

    def setUp(self):
        us= User.objects.filter(id=1).first()

        tgm1= Etiqueta.objects.create(nom='I+D',descripcio= 'recursos relacionados con el I+D',usuari=us, tipologia = 'M')
        tgm2= Etiqueta.objects.create(nom='Bibliografia',descripcio= 'recursos relacionados con la Bibliografia',usuari=us, tipologia = 'M')
        tgm3= Etiqueta.objects.create(nom='Informes',descripcio= 'recursos estadisticos, unicamente informes',usuari=us, tipologia = 'M')
        tgm4= Etiqueta.objects.create(nom='Experiencias',descripcio= 'Paginas de blog donde se habla de experiencias personales relacionadas',usuari=us, tipologia = 'M')

        R1 = Recurs.objects.create(url='www.reddit.com', descripcio='Sitio de encuentro de experiencias',usuari=us,cela=c1)
        R2 = Recurs.objects.create(url='www.youtube.com', descripcio='Sitio dedicado al video',usuari=us,cela=c1)
        R3 = Recurs.objects.create(url='www.m1l3.net/Blog', descripcio='Blog personal dedicado a la tecnologia',usuari=us,cela=c1)
        R4 = Recurs.objects.create(url='www.Django.com', descripcio='Inovación i desarrollo en el ambito de la creación de software',usuari=us,cela=c1)
        R5 = Recurs.objects.create(url='www.miblog.es', descripcio='Blog de experiencias personales de un viajero',usuari=us,cela=c1)
        R6 = Recurs.objects.create(url='www.miexperiencia.com', descripcio='Biblioteca de experiencias colectivas',usuari=us,cela=c1)
        R7 = Recurs.objects.create(url='www.todoI+D.net', descripcio='Referencias a proyectod de inovación',usuari=us,cela=c1)
        R8 = Recurs.objects.create(url='www.ordenadores.net', descripcio='Todo sobre ordenadores, wiki colaborativa de reparación de hardware',usuari=us,cela=c1)

        R1.save()
        R1.etiquetes.add(tgm1)
        R1.etiquetes.add(tgm2)
        R2.save()
        R2.etiquetes.add(tgm4)
        R2.etiquetes.add(tgm2)
        R3.save()
        R3.etiquetes.add(tgm4)
        R3.etiquetes.add(tgm1)
        R4.save()
        R4.etiquetes.add(tgm3)
        R4.etiquetes.add(tgm1)
        R5.save()
        R5.etiquetes.add(tgm4)
        R5.etiquetes.add(tgm2)
        R6.save()
        R6.etiquetes.add(tgm4)
        R7.save()
        R7.etiquetes.add(tgm1)
