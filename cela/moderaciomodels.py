# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from rusc.post.models import Post



#Classe per controlar els missatges de moderació
class ModeracioMissatge(models.Model):
    usuari = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    text = models.TextField()
    datahora =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

#http://stackoverflow.com/questions/20895429/how-exactly-do-django-content-types-work