from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import User

#Classe per controlar els missatges de moderació
class ModComment(models.Model):
    author = models.ForeignKey(User)
    body = models.TextField(blank=True)
    datahora = models.DateTimeField(auto_now=True)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.body

  #http://stackoverflow.com/questions/20895429/how-exactly-do-django-content-types-work