__author__ = 'Zartch'
from django.contrib.auth.models import User
from django.db import models
from post.models import Post
from cela.models import Cela
from django.shortcuts import render,get_object_or_404,redirect

class UserProfile(models.Model):

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
    user = models.ForeignKey(User)
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    avatar = models.ImageField(upload_to='/Usuario/profile_images', blank=True)
    subscripcions = models.ManyToManyField(Post,blank=True, related_name="subscripcions")
    tipusSubscripcio = models.CharField(max_length=1,choices= TIPUS_SUBSCRIPCIO,default='S')
    cela= models.ForeignKey(Cela)
    estat = models.CharField(max_length=1, choices=ESTAT_SUBSCRIPCIO, default='A')
    mailConf = models.CharField(max_length=1,choices=ENVIAMENT_MAIL,default='E')


    #añadido para referenciar al objeto de usuario #ToDo Saber exactamente que es esto
    #http://stackoverflow.com/questions/8177289/django-profiles
    #User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0]0

    def __str__(self):
        return self.user.username

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
    if cela_pk != 'NoCell':
        cela = get_object_or_404(Cela, pk=cela_pk)

        #control per que el estat dels usuaris a les celes no publiques es crein correctament
        if cela.tipus != 'P':
            profile = UserProfile(user = user, cela = cela, estat='E')
        else:
            profile = UserProfile(user = user, cela = cela)

        profile.save()
user_registered.connect(user_registered_callback)

