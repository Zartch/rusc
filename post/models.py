from django.db import models
from django.contrib.auth.models import User
from recurs.models import Recurs
from etiqueta.models import Etiqueta
from django.core.urlresolvers import reverse
from cela.models import Cela,get_cela

#classe que gestiona(manager) els vots dels diferents posts. camp 'with_votes' del post
from django.db.models import Count
from django.utils.timezone import now

class PostVoteCountManager(models.Manager):

    def get_queryset(self):
        return super(PostVoteCountManager, self).get_queryset().annotate(votes=Count('votePost')
        )


#La Barra per comentar es "/"
#He solucionat això a Recurs
# class PostRecurs(models.Model):
#
#     TIPUS_RELACIO = (
#         ('R','Referent A'),
#     )
#
#     post = models.ForeignKey('Post')
#     recurs = models.ForeignKey(Recurs)
#     tipus = models.CharField(max_length=1,choices=TIPUS_RELACIO, blank=True,default="")
#
#     def __str__(self):
#         return self.etq1 + self.etq2 + self.tipo


class Post(models.Model):

    ESTAT_MODERACIO = (
        ('A','Aprobat'),
        ('R','Rebutjat'),
        ('E','En Tramit'),
    )

    moderacio= models.CharField(max_length=1,choices=ESTAT_MODERACIO, default='E')
    titol = models.CharField(max_length=40)
    text = models.TextField()
    pare = models.ForeignKey('self', related_name='children', blank=True, null=True)
    datahora =models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User)
    recursos = models.ManyToManyField(Recurs, blank=True)
    etiquetes = models.ManyToManyField(Etiqueta, blank=True)
    cela = models.ForeignKey(Cela,blank=True)

    with_votes =PostVoteCountManager()
    objects = models.Manager()

    def __str__(self):
        return self.titol
 #args=[str(self.id)]
    def get_absolute_url(self):
        return reverse('post', args=[str(self.get_root())] )

    #función que dibuja todos los nodos en forma de arbol
    def as_tree(self):
        children = list(self.children.all())
        branch = bool(children)
        #http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do-in-python
        yield branch, self
        for child in children:
            for next in child.as_tree():
                yield next
        yield branch, None

    #Busquem el inici del arbre per a mostrar la conversa útil per a respondre
    #ToDo Millorar aquest algoritme per que mostri només un resultat significant no infinit (per exemple, mentre el titol continui sent igual)
    def get_root(self):
        if self.pare == None:
            return self.pk
        else:
            comment_root = self.pare
            while comment_root.pare != None:
                comment_root = comment_root.pare
            return comment_root.pk

    def get_root_object(self):
        if self.pare == None:
            return self.pk
        else:
            comment_root = self.pare
            while comment_root.pare != None:
                comment_root = comment_root.pare
            return comment_root

    #Llistat de usuaris subscrits al root de un post
    def get_subscriptors(self):
        post = self.get_root_object()
        users = User.objects.filter(userprofile__subscripcions = post)
        users_cela = User.objects.filter(userprofile__tipusSubscripcio = 'T', userprofile__cela = self.cela)
        user_subscrits = []
        for user in users:
            user_subscrits.append(user)
        for user in users_cela:
            user_subscrits.append(user)
        return user_subscrits

    def set_rank(self):
        # Based on HN ranking algo at http://amix.dk/blog/post/19574
        SECS_IN_HOUR = float(60*60)
        GRAVITY = 1.2

        delta = now() - self.datahora
        item_hour_age = delta.total_seconds() // SECS_IN_HOUR
        votes = self.votes - 1
        self.rank_score = votes / pow((item_hour_age+2), GRAVITY)
        self.save()

# from django.db.models.signals import post_save
#
#
# def post_handler(sender, instance, created, **kwargs):
#
#
# post_save.connect(post_handler, sender=Post)

class Vote(models.Model):
    voter = models.ForeignKey(User)
    post = models.ForeignKey(Post, related_name='votePost')

    def __str__(self):
        return "%s voted %s" % (self.voter.username, self.post.titol)
