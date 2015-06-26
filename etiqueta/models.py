from django.db import models
from django.contrib.auth.models import User
from cela.models import Cela

class Etiqueta(models.Model):

    TIPO_TIPOLOGIA = (
        ('S', 'Sistema'),
        ('M', 'Moderacion'),
        ('E', 'Etiqueta'),
        ('O', 'Objecte'), #persona o cosa
        ('A', 'Adjectiu'),
        ('T', 'Temps'),
        ('L', 'Lloc'),
    )

    ESTAT_MODERACIO = (
        ('A','Aprobat'),
        ('R','Rebutjat'),
        ('E','En Tramit'),
    )

    moderacio= models.CharField(max_length=1,choices=ESTAT_MODERACIO, default='E')
    nom = models.CharField(max_length=100)
    tipologia = models.CharField(max_length=1, choices=TIPO_TIPOLOGIA, default='E')
    #descripcio = models.TextField(verbose_name=('descripció'), blank=True) #Será un enllaç a la wikipedia
    wiki = models.URLField(blank=True, default="")
    #usuari = models.ForeignKey(User)
    datahora =models.DateTimeField(auto_now_add=True)
    cela = models.ForeignKey(Cela,blank=True)
    relacio = models.ManyToManyField('Etiqueta', through='Tesauro', blank=True)
    #Cam per a reflexar un valor que podrá ser considerat com un camp de el model,
    #Les estiquees que es creein amb paraula:valor es separaran en nom i valor
    #valor = models.CharField(max_length=25, blank=True)

    def get_list(self):

        li = [self.etq1,self.etq2]
        return li



    def __str__(self):
        return self.nom

class Tesauro(models.Model):

    #ToDo Millorar com Tesauro/ontologia
    #http://es.wikipedia.org/wiki/Tesauro
    TIPUS_TESAURO = (
        ('J','jerarquic'),
        ('S','sinonims'),
        ('A','antonims'),
        ('B','associatiu'),
    )


    # etq = list(models.ForeignKey(Etiqueta, related_name="element"))

    etq1 = models.ForeignKey(Etiqueta, related_name="element_fort")
    etq2 = models.ForeignKey(Etiqueta, related_name="element_debil")

    tipo = models.CharField(max_length=1,choices=TIPUS_TESAURO)


    def __str__(self):
        return self.etq1.nom + self.etq2.nom + self.tipo



