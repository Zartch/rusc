# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from post.models import Post
from cela.models import Cela
from django.shortcuts import render,get_object_or_404,redirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

class UserProfile(models.Model):

    #La imatge del avatar no pot ser de més de 5Mb
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 2.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


    TIPUS_SUBSCRIPCIO = (
        ('T','Total'),
        ('S','Nomes subscrits. Subscriure automaticament'),
        ('X','Nomes subscrits: No subscriure automaticament') #Despres de contestar a un post
    )

    ESTAT_SUBSCRIPCIO = (
        ('A','Acceptat'),
        ('E','En Tramit'),
        ('R','Rebutjat'),
        ('T','Troll'),
    )

    ENVIAMENT_MAIL= {
        ('E','Enviar Tots el Mails'),
        ('N','No Enviar Mails'),
    }

    # This line is required. Links UserProfile to a User model instance.
    user = models.ForeignKey(User, null=True )
    # The additional attributes we wish to include.
    website = models.URLField(null=True)
    avatar = models.FileField(upload_to='profiles/%Y/%m/%d', null=True, validators=[validate_image])
    subscripcions = models.ManyToManyField(Post,blank=True, related_name="subscripcions")
    tipusSubscripcio = models.CharField(max_length=1,choices= TIPUS_SUBSCRIPCIO,default='S')
    cela= models.ForeignKey(Cela)
    estat = models.CharField(max_length=1, choices=ESTAT_SUBSCRIPCIO, default='A')
    mailConf = models.CharField(max_length=1,choices=ENVIAMENT_MAIL,default='E')
    #Aquest camp serveix per a guardarnos el email dels usuaris convidats que encara no estan
    #registrats a RUSC. Quan es registrin sels incloura directament a la cela
    email_p = models.EmailField(blank=True)


    class Meta:
        unique_together = (("cela", "user"),)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('forum')

    #Sempre subscriurem al post root
    def subscriure(self, post_pk):
        result = True
        post = Post.objects.filter(pk=post_pk).first()
        post_afegir_pk = post.get_root()
        post_afegir = Post.objects.filter(pk=post_afegir_pk).first()
        self.subscripcions.add(post_afegir)

        return result


from registration.signals import user_registered

def user_registered_callback(sender, user, request, **kwargs):
    cela_pk = request.session.get('cell', 'NoCell')
    #Preguntem si el e-mail ja está associat a algún userprofile per afergir les celes
    # a las que s'ha convidat
    Up = UserProfile.objects.filter(email_p = user.email)
    for userp in Up:
        userp.user = user
        userp.save()

    if cela_pk != 'NoCell':
        cela = get_object_or_404(Cela, pk=cela_pk)

        #control per que el estat dels usuaris a les celes no publiques es crein correctament
        #Alimentem el camp email_p del user profile pq ens serveix per a crear la clau primaria de la taula UserProfile
        if cela.tipus != 'P':
            profile = UserProfile(user = user, cela = cela, estat='E',email_p= user.email)
        else:
            profile = UserProfile(user = user, cela = cela, email_p= user.email)

        profile.save()
user_registered.connect(user_registered_callback)






