from django.contrib import admin

from rusc.recurs.models import Recurs

# Register your models here.

class recursAdmin(admin.ModelAdmin):
    list_display = ('url','moderacio','cela')
    search_fields = ['url']
    list_filter = ['url']
    filter_horizontal = ('etiquetes',)

admin.site.register(Recurs, recursAdmin)