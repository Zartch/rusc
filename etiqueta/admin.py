from django.contrib import admin
from etiqueta.models import Etiqueta
# Register your models here.

class etiquetaAdmin(admin.ModelAdmin):
    list_display = ('nom','descripcio','tipologia','usuari')
    search_fields = ['nom','descripcio','tipologia']
    list_filter = ['nom','tipologia']
    filter_horizontal = ('relacio',)
admin.site.register(Etiqueta, etiquetaAdmin)