# -*- coding: utf-8 -*-
import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor
from rusc.etiqueta.models import Tesauro, Etiqueta

TEMPLATEEDIT_tesauro = '''
   <a href="{% url 'mod_tesauro' record.pk  %}"> Edit </a>
'''
TEMPLATEDELETE_tesauro = '''
   <a href="{% url 'delete_tesauro' record.pk %}"> Delete </a>
'''

class tesauroTable(tables.Table):
    etq1 = tables.LinkColumn('etiqueta', args=[A('pk')])
    etq2 = tables.LinkColumn('etiqueta', args=[A('pk')])
    #edit_link = tables.LinkColumn('cliente:clientMod', args=[A('pk')], verbose_name='edit', accessor='pk')
    #delete_link = tables.LinkColumn('cliente:client_delete', args=[A('pk')], verbose_name='delete',)
    Edit = tables.TemplateColumn(TEMPLATEEDIT_tesauro)
    Delete = tables.TemplateColumn(TEMPLATEDELETE_tesauro)
    class Meta:
        model = Tesauro
        # add class="paleblue" to <table> tag
        attrs = {"class": "table table-striped"}


TEMPLATEEDIT_etq = '''
   <a href="{% url 'mod_etiqueta' record.pk  %}"> Edit </a>
'''
TEMPLATEDELETE_etq = '''
   <a href="{% url 'delete_etiqueta' record.pk %}"> Delete </a>
'''

class etiquetaTable(tables.Table):
    nom = tables.Column('nom')
    tipologia = tables.Column('tipologia')
    descripcio = tables.Column('descripcio')
    wiki = tables.URLColumn('wiki')
    Edit = tables.TemplateColumn(TEMPLATEEDIT_etq)
    Delete = tables.TemplateColumn(TEMPLATEDELETE_etq)

    class Meta:
        model = Etiqueta
        # add class="paleblue" to <table> tag
        attrs = {"class": "table table-striped"}

