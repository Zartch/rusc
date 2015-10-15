from post.models import Post
from django.contrib.auth.models import User
from django.db import models


#Classe per controlar els missatges de moderació
class ModeracioMissatge(models.Model):
    usari = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    text = models.TextField()
    datahora =models.DateTimeField(auto_now_add=True)