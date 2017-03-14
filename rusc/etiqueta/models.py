# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.template.defaultfilters import slugify

from cela.models import Cela, TipoEtiqueta
import django_filters
#from rusc.ficha.models import Ficha


class EtiquetaManager(models.Manager):

    def zona(self,cela):
        return self.filter(tipologia = 'Z', cela= cela)

    def seccion(self, cela, zona):
        return self.filter(tipologia = 'M', cela= cela)


class Etiqueta(models.Model):

    TIPO_TIPOLOGIA = (
        ('S', 'Sistema'),#
        ('M', 'Moderacion'),#Para los grupos de recursos
        ('Z', 'AreaContexto'),# Zona de aportación, contexto y otras
        ('E', 'Etiqueta'), #Las etiquetas en general
        ('O', 'Objecte'), #persona o cosa
        ('A', 'Adjectiu'), #Adjetivaciones
        ('T', 'Temps'), #tiempo
        ('L', 'Lloc'), #Lugar
        ('P', 'Profesion')
    )

    ESTAT_MODERACIO = (
        ('A','Aprobat'),
        ('R','Rebutjat'),
        ('E','En Tramit'),
    )

    moderacio= models.CharField(max_length=1,choices=ESTAT_MODERACIO, default='E')
    nom = models.CharField(max_length=100)
    slug = models.CharField(blank=True, max_length=100)
    #tipologia = models.CharField(max_length=1, choices=TIPO_TIPOLOGIA, default='E')
    tipologia = models.ForeignKey(TipoEtiqueta, null=True)
    descripcio = models.TextField(verbose_name=('descripció'), blank=True) #Será un enllaç a la wikipedia
    wiki = models.URLField(blank=True, default="")
    #usuari = models.ForeignKey(User)
    datahora =models.DateTimeField(auto_now_add=True)
    cela = models.ForeignKey(Cela,blank=True)
    relacio = models.ManyToManyField('Etiqueta', through='Tesauro', blank=True)
    #Campos adicionales que tendrán que contener los recursos:
    #solo las etiquetas de tipo M tendrán fichas
    ficha = models.ManyToManyField('Ficha', related_name = 'datosAdicionales')

    objects = EtiquetaManager()

    def __str__(self):
        return 'a'

    def __unicode__(self):
        return 'b'

    def get_list_tesauros(self):
        tesauros = Tesauro.objects.filter(Q(etq1=self)|Q(etq2=self))
        etq_lst = dict()
        for relacio in tesauros:
            if (relacio.etq1.nom != self.nom):
                if relacio.etq1.nom in etq_lst.keys():
                    valor = etq_lst[relacio.etq1]
                    valor = valor +1
                    etq_lst[relacio.etq1]  = valor
                else:
                    etq_lst[relacio.etq1] = 1
            else:
                if relacio.etq2.nom in etq_lst.keys():
                    valor = etq_lst[relacio.etq2]
                    valor = valor +1
                    etq_lst[relacio.etq2]  = valor
                else:
                    etq_lst[relacio.etq2] = 1

        return etq_lst

    def get_subdits(self):
        pks = Tesauro.objects.filter(etq1=self).values_list('etq2',flat=True)
        subdits = Etiqueta.objects.filter(pk__in=pks).all()
        return subdits

    def __str__(self):
        return self.nom


class EtiquetaFilter(django_filters.FilterSet):
    class Meta:
        model = Etiqueta
        fields = ['nom', 'tipologia', 'descripcio','wiki']

def jsonSubdits(etq, maxRec = 10):
    json = {}
    if maxRec >0:
        maxRec -= 1
        json['name']= etq.nom
        json['size']= 800
        json['children'] = []

        for subdit in etq.get_subdits():
            fills = json['children']
            fills.append(jsonSubdits(subdit,maxRec))
            json['children'] = fills
    return json


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


class TesauroFilter(django_filters.FilterSet):
    class Meta:
        model = Tesauro
        fields = ['etq1', 'etq2', 'tipo']


class Ficha(models.Model):
    etq = models.ForeignKey(Etiqueta, related_name='ficha_etq') #Etiqueta tipo M
    tipo = models.ForeignKey(TipoEtiqueta) #El dato obligatorio
    descrip = models.CharField(max_length=80) #Dato para cambiar el nombre
    obliatorio = models.BooleanField(default=False)
    hint = models.CharField(max_length=80) #explicación del campo

    def __str__(self):
        return " Ficha: '" + self.etq + "'" + " :"+ self.tipo






def etiqueta_post_save(sender, instance, created, *args, **kwargs):
    """Argument explanation:

       sender - The model class. (MyModel)
       instance - The actual instance being saved.
       created - Boolean; True if a new record was created.

       *args, **kwargs - Capture the unneeded `raw` and `using`(1.3) arguments.
    """
    #canviar per if created ==True; si nomes volem que s'executi la primera vegada que es crea
    if created:
        instance.slug = slugify(instance.nom)
        instance.save()


from django.db.models.signals import post_save
post_save.connect(etiqueta_post_save, sender=Etiqueta)
