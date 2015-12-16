# -*- coding: utf-8 -*-
from django.contrib import admin
from cela.models import Cela

# Register your models here.

class celaAdmin(admin.ModelAdmin):
    list_display = ('pregunta','datacreacio')
    search_fields = ['pregunta','datacreacio','moderadors']
    list_filter = ['pregunta','datacreacio','moderadors']
    filter_horizontal = ('moderadors',)
admin.site.register(Cela, celaAdmin)