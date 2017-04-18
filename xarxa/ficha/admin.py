from xarxa.ficha.models import Ficha, CamposFicha
from django.contrib import admin

class fichaAdmin(admin.ModelAdmin):
    list_display =  ('nom', 'cela')
    search_fields =  ['nom']
    list_filter = ['cela']

admin.site.register(Ficha, fichaAdmin)


class fichaCampsAdmin(admin.ModelAdmin):
    list_display =  ('descrip', 'ficha','obliatorio','hint')
    search_fields =  ['nom']
    list_filter = ['ficha']

admin.site.register(CamposFicha, fichaCampsAdmin)