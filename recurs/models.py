from django.db import models
from django.contrib.auth.models import User
from etiqueta.models import Etiqueta
from cela.models import Cela



class Recurs(models.Model):

    ESTAT_MODERACIO = (
        ('A','Aprobat'),
        ('R','Rebutjat'),
        ('E','En Tramit'),
    )

    moderacio= models.CharField(max_length=1,choices=ESTAT_MODERACIO, default='E')
    url = models.TextField()
    descripcio = models.TextField(blank=True)
    #usuari = models.ForeignKey(User)
    etiquetes = models.ManyToManyField(Etiqueta,blank=True)
    datahora = models.DateTimeField(auto_now_add=True)
    autor =  models.CharField(max_length=100,blank=True)
    cela = models.ForeignKey(Cela,blank=True)
    post_debat = models.ForeignKey("post.Post",verbose_name="recurs",  null=True)

    def __str__(self):
        return self.url



