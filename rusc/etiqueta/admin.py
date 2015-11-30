from django.contrib import admin

from rusc.etiqueta.models import Etiqueta, Tesauro

# Register your models here.

class etiquetaAdmin(admin.ModelAdmin):
    list_display = ('pk','nom','wiki','tipologia','cela')
    search_fields = ['nom','wiki','tipologia']
    list_filter = ['cela','tipologia']
    filter_horizontal = ('relacio',)
admin.site.register(Etiqueta, etiquetaAdmin)

class tesauroAdmin(admin.ModelAdmin):
    list_display = ('pk','etq1','etq2','tipo')
    search_fields = ['etq1','etq2','tipo']
    list_filter = ['etq1','etq2','tipo']


admin.site.register(Tesauro, tesauroAdmin)