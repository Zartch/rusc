# -*- coding: utf-8 -*-
import datetime

from django.db import models
from django.contrib.auth.models import User

from cela.models import Cela


class Pregunta(models.Model):

    text = models.TextField()
    answer = models.TextField(blank=True)
    sort_order = models.IntegerField(default=0)
    created_on = models.DateTimeField(default=datetime.datetime.now)
    updated_on = models.DateTimeField(default=datetime.datetime.now)
    created_by = models.ForeignKey(User,null=True, related_name= 'pregunta_created')
    updated_by = models.ForeignKey(User,null=True, related_name= 'pregunta_updated')
    cela = models.ForeignKey(Cela, related_name= 'cela_FAQ')