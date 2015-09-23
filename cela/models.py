# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
#from etiqueta.models import Etiqueta
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages as notif_messages


class Cela(models.Model):

    #Privada no surt a les cerques, Registrats si
    TIPUS_CELA = (
        ('P','Publica'),
        ('X','Privada'), #Acceptan peticións de ingres Moderadors
        ('R','Registrats'), #Acceptan tots
    )

    TIPUS_MODERACIO = (

    )

    pregunta = models.CharField(max_length=70)
    datacreacio = models.DateTimeField(auto_now_add=True)
    #etiquetes = models.ManyToManyField('Etiqueta', blank=True)
    moderadors = models.ManyToManyField(User)
    descripcio= models.TextField()
    tipus = models.CharField(max_length=1,choices=TIPUS_CELA)

    def __str__(self):
        return self.pregunta

    def get_absolute_url(self):
        return reverse('cela', args=[self.pk] )


    # def save(self, force_insert=False, force_update=False, using=None,
    #          update_fields=None):
    #
    #     for mod in self.moderadors.all():
    #         create_userProfile(mod, self)
    #     notif_messages.add_message(self.request, notif_messages.INFO, "Has creat una nova cela", 'success')

def get_cela(request):
    cela_pk = request.session.get('cell', 'NoCell')
    if cela_pk == 'NoCell' or not request.user.is_authenticated():
         return '0'
    cela = get_object_or_404(Cela, pk=cela_pk)

    return cela




