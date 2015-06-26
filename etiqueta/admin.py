from django.contrib import admin
from etiqueta.models import Etiqueta, Tesauro
# Register your models here.

class etiquetaAdmin(admin.ModelAdmin):
    list_display = ('pk','nom','wiki','tipologia','cela')
    search_fields = ['nom','wiki','tipologia']
    list_filter = ['nom','tipologia']
    filter_horizontal = ('relacio',)
admin.site.register(Etiqueta, etiquetaAdmin)

class tesauroAdmin(admin.ModelAdmin):
    list_display = ('pk','etq','tipo')
    search_fields = ['etq','tipo']
    list_filter = ['etq','tipo']
admin.site.register(Tesauro, tesauroAdmin)