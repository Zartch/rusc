# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from etiqueta.models import Etiqueta
from cela.models import Cela
from django.core.exceptions import ValidationError


class Recurs(models.Model):

    def validate_file(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    ESTAT_MODERACIO = (
        ('A','Aprobat'),
        ('R','Rebutjat'),
        ('E','En Tramit'),
    )

    moderacio= models.CharField(max_length=1,choices=ESTAT_MODERACIO, default='E')
    url = models.TextField()
    descripcio = models.TextField(blank=True, default="")
    #usuari = models.ForeignKey(User)
    etiquetes = models.ManyToManyField(Etiqueta,blank=True)
    datahora = models.DateTimeField(auto_now_add=True)
    autor =  models.CharField(max_length=100,blank=True, default='')
    cela = models.ForeignKey(Cela,blank=True)
    post_debat = models.ForeignKey("post.Post",verbose_name="recurs",  null=True)
    adjunt = models.FileField(upload_to='documents/%Y/%m/%d', null=True, validators=[validate_file])

    def __str__(self):
        return self.url



