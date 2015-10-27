import django_tables2 as tables
from django_tables2.utils import A  # alias for Accessor

from rusc.etiqueta.models import Tesauro


TEMPLATEEDIT = '''
   <a href="{% url 'mod_tesauro' record.pk  %}"> Edit </a>
'''
TEMPLATEDELETE = '''
   <a href="{% url 'delete_tesauro' record.pk %}"> Delete </a>
'''

class tesauroTable(tables.Table):
    etq1 = tables.LinkColumn('etiqueta', args=[A('pk')])
    etq2 = tables.LinkColumn('etiqueta', args=[A('pk')])
    #edit_link = tables.LinkColumn('cliente:clientMod', args=[A('pk')], verbose_name='edit', accessor='pk')
    #delete_link = tables.LinkColumn('cliente:client_delete', args=[A('pk')], verbose_name='delete',)
    Edit = tables.TemplateColumn(TEMPLATEEDIT)
    Delete = tables.TemplateColumn(TEMPLATEDELETE)
    class Meta:
        model = Tesauro
        # add class="paleblue" to <table> tag
        attrs = {"class": "table table-striped"}


