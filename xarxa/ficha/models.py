# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from cela.models import Cela


class Ficha(models.Model):

    nom = models.CharField(max_length=100)
    descripcion  = models.TextField()
    cela = models.ForeignKey(Cela)

    def __str__(self):
        return self.nom



class CamposFicha(models.Model):

    ficha = models.ForeignKey(Ficha)
    descrip = models.CharField(max_length=80) #Dato para cambiar el nombre
    obliatorio = models.BooleanField(default=False)
    hint = models.CharField(max_length=80, blank=True, default='') #explicación del campo
    #regex = models.CharField(max_length=60)

    def __str__(self):
        return str(self.descrip)
