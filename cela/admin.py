# -*- coding: utf-8 -*-
from django.contrib import admin
from cela.models import Cela, Tema, TipoEtiqueta

# Register your models here.

class celaAdmin(admin.ModelAdmin):
    list_display = ('pregunta','datacreacio','get_temas')
    search_fields = ['pregunta','datacreacio','moderadors']
    list_filter = ['pregunta','datacreacio','moderadors']
    filter_horizontal = ('moderadors','temas')


class temaAdmin(admin.ModelAdmin):
    list_display = ('nom','slug')
    search_fields = ['nom']
    list_filter = ['nom']



class TipoEtiquetaAdmin(admin.ModelAdmin):
    list_display = ('nom','pk')
    search_fields = ['nom']
    list_filter = ['nom']


admin.site.register(Tema, temaAdmin)
admin.site.register(TipoEtiqueta, TipoEtiquetaAdmin)
admin.site.register(Cela, celaAdmin)