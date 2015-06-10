from django.contrib import admin
from cela.models import Cela
# Register your models here.

class celaAdmin(admin.ModelAdmin):
    list_display = ('pregunta','datacreacio')
    search_fields = ['pregunta','datacreacio','moderadors']
    list_filter = ['pregunta','datacreacio','moderadors']

admin.site.register(Cela, celaAdmin)