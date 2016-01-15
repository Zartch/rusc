# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
#from etiqueta.models import Etiqueta
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages as notif_messages
from django.template.defaultfilters import slugify


class Cela(models.Model):

    #Privada no surt a les cerques, Registrats si
    TIPUS_CELA = (
        ('P','Visible'),
        ('X','Invisible'), #Acceptan peticións de ingres Moderadors
        ('R','Supervisada'), #Acceptan tots
    )

    TIPUS_MODERACIO = (

    )

    pregunta = models.CharField(max_length=70)
    slug = models.CharField(blank=True, max_length=100)
    datacreacio = models.DateTimeField(auto_now_add=True)
    #etiquetes = models.ManyToManyField('Etiqueta', blank=True)
    moderadors = models.ManyToManyField(User)
    descripcio= models.TextField()
    tipus = models.CharField(max_length=1,choices=TIPUS_CELA, default='P')

    def __str__(self):
        return self.pregunta

    def get_absolute_url(self):
        return reverse('cela', args=[self.pk] )

    def get_etiquetes(self):
        posts = self.posts.all()
        etiquetes = set()
        for post in posts:
            for etq in post.etiquetes.all():
                etiquetes.add(etq)
        return etiquetes





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

#http://www.b-list.org/weblog/2006/nov/02/django-tips-auto-populated-fields/
# class cela_manager(models.Manager):
#     def new_cela_user(self, user):
#         new_cela = self.model(moderador = user)


def cela_post_save(sender, instance, created, *args, **kwargs):
    """Argument explanation:

       sender - The model class. (MyModel)
       instance - The actual instance being saved.
       created - Boolean; True if a new record was created.

       *args, **kwargs - Capture the unneeded `raw` and `using`(1.3) arguments.
    """
    #canviar per if created ==True; si nomes volem que s'executi la primera vegada que es crea
    if created:
        instance.slug = slugify(instance.pregunta)
        instance.save()


from django.db.models.signals import post_save
post_save.connect(cela_post_save, sender=Cela)